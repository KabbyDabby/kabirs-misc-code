import os
import requests
import time
from pathlib import Path
from urllib.parse import urljoin, urlparse
import re
from typing import List, Dict, Optional
import json
import logging
from bs4 import BeautifulSoup
import anthropic
from datetime import datetime
import random

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CDSDownloader:
    def __init__(self, api_key: str, download_folder: str = "CDS PDFs"):
        """
        Initialize the CDS Downloader with Claude API key
        
        Args:
            api_key: Your Claude API key
            download_folder: Folder to save downloaded CDS files
        """
        self.client = anthropic.Anthropic(api_key=api_key)
        self.download_folder = Path(download_folder)
        self.download_folder.mkdir(exist_ok=True)
        
        # File extensions to look for
        self.file_extensions = ['.pdf', '.xlsx', '.xls', '.doc', '.docx']
        
        # Current year for finding most recent CDS
        self.current_year = datetime.now().year
        
    def google_search_cds(self, college_name: str) -> List[str]:
        """
        Use Claude to perform a Google search for CDS files
        
        Args:
            college_name: Name of the college
            
        Returns:
            List of potential CDS URLs from Google search results
        """
        # Add retry mechanism
        max_retries = 3
        retry_delay = 5
        
        for attempt in range(max_retries):
            try:
                # Construct Google search URL
                search_query = f'"{college_name}" "Common Data Set" filetype:pdf OR site:edu'
                google_url = f"https://www.google.com/search?q={search_query.replace(' ', '+')}"
                
                # Add more realistic headers
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'DNT': '1',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1'
                }
                
                # Add random delay between requests
                time.sleep(random.uniform(2, 5))
                
                response = requests.get(google_url, headers=headers, timeout=10)
                response.raise_for_status()
                
                # Force UTF-8 encoding
                response.encoding = 'utf-8'
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Extract search results
                search_results = []
                result_divs = soup.find_all('div', class_='g')
                
                for div in result_divs[:10]:  # Get first 10 results
                    try:
                        link_elem = div.find('a')
                        if link_elem and link_elem.get('href'):
                            url = link_elem.get('href')
                            if url.startswith('/url?q='):
                                # Extract actual URL from Google redirect
                                url = url.split('/url?q=')[1].split('&')[0]
                            
                            title_elem = div.find('h3')
                            title = title_elem.get_text() if title_elem else ""
                            
                            search_results.append({
                                'title': title,
                                'url': url
                            })
                    except Exception as e:
                        logger.warning(f"Error processing search result: {e}")
                        continue
                
                # Use Claude to analyze search results and pick the best ones
                if search_results:
                    results_text = "\n".join([f"{r['title']}: {r['url']}" for r in search_results])
                    
                    prompt = f"""
                    I searched Google for "{college_name} Common Data Set" and got these results:
                    
                    {results_text}
                    
                    Please identify the URLs that are most likely to be official Common Data Set files from {college_name}. 
                    Prioritize:
                    1. Official university websites (.edu domains)
                    2. Recent years (2023, 2024, 2025)
                    3. Direct PDF links or pages that likely contain CDS downloads
                    4. Institutional research or admissions pages
                    
                    Return only the URLs, one per line, starting with the most promising ones.
                    """
                    
                    message = self.client.messages.create(
                        model="claude-sonnet-4-20250514",
                        max_tokens=1000,
                        messages=[{"role": "user", "content": prompt}]
                    )
                    
                    # Extract URLs from Claude's response
                    response_text = message.content[0].text
                    potential_urls = []
                    
                    for line in response_text.split('\n'):
                        line = line.strip()
                        if line.startswith('http'):
                            potential_urls.append(line)
                        elif 'http' in line:
                            # Extract URLs from lines that contain them
                            url_match = re.search(r'https?://[^\s]+', line)
                            if url_match:
                                potential_urls.append(url_match.group())
                    
                    return potential_urls
                
                return []
                
            except Exception as e:
                logger.error(f"Error in Google search attempt {attempt + 1}: {e}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay * (attempt + 1))  # Exponential backoff
                    continue
                raise
    
    def find_most_recent_cds_on_page(self, url: str) -> List[Dict[str, str]]:
        """
        Search a specific page for the most recent CDS files
        
        Args:
            url: URL to search
            
        Returns:
            List of dictionaries with file info (name, url, year)
        """
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            cds_files = []
            
            # Look for links to files
            for link in soup.find_all('a', href=True):
                href = link.get('href')
                link_text = link.get_text().strip()
                
                if not href:
                    continue
                    
                full_url = urljoin(url, href)
                
                # Check if this looks like a CDS file
                combined_text = (link_text + ' ' + href).lower()
                
                # Look for CDS indicators and years
                has_cds_indicators = any(keyword in combined_text for keyword in [
                    'common data set', 'cds', 'factbook', 'institutional research'
                ])
                
                # Check for file extensions
                has_valid_extension = any(href.lower().endswith(ext) for ext in self.file_extensions)
                
                # Extract year from text or URL
                year_matches = re.findall(r'20\d{2}', combined_text)
                year = max([int(y) for y in year_matches]) if year_matches else 0
                
                if has_cds_indicators and (has_valid_extension or 'pdf' in href.lower()):
                    cds_files.append({
                        'name': link_text or os.path.basename(href),
                        'url': full_url,
                        'year': year
                    })
            
            # Sort by year (most recent first) and return
            cds_files.sort(key=lambda x: x['year'], reverse=True)
            return cds_files
            
        except Exception as e:
            logger.error(f"Error searching page {url}: {e}")
            return []
    
    def download_file(self, file_info: Dict[str, str], college_name: str) -> bool:
        """
        Download a CDS file
        
        Args:
            file_info: Dictionary with file name, URL, and year
            college_name: Name of the college for folder organization
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Create college-specific folder
            college_folder = self.download_folder / college_name.replace(' ', '_').replace('/', '_')
            college_folder.mkdir(exist_ok=True)
            
            # Get file extension from URL
            parsed_url = urlparse(file_info['url'])
            file_extension = os.path.splitext(parsed_url.path)[1]
            
            if not file_extension:
                # Try to determine from content-type
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
                try:
                    head_response = requests.head(file_info['url'], headers=headers, timeout=10)
                    content_type = head_response.headers.get('content-type', '').lower()
                    if 'pdf' in content_type:
                        file_extension = '.pdf'
                    elif 'excel' in content_type or 'spreadsheet' in content_type:
                        file_extension = '.xlsx'
                    else:
                        file_extension = '.pdf'  # Default assumption
                except:
                    file_extension = '.pdf'  # Default if HEAD request fails
            
            # Create filename with year if available
            safe_filename = re.sub(r'[^\w\s-]', '', file_info['name'])
            safe_filename = re.sub(r'[-\s]+', '-', safe_filename)
            
            year_suffix = f"_{file_info['year']}" if file_info.get('year', 0) > 2000 else ""
            filename = f"CDS_{college_name.replace(' ', '_')}{year_suffix}{file_extension}"
            filepath = college_folder / filename
            
            # Download the file
            logger.info(f"Downloading {file_info['name']} from {file_info['url']}")
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(file_info['url'], headers=headers, timeout=30)
            response.raise_for_status()
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            logger.info(f"Successfully downloaded: {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Error downloading {file_info['name']}: {e}")
            return False
    
    def process_college(self, college_name: str) -> Dict[str, any]:
        """
        Process a single college to find and download the most recent CDS file
        
        Args:
            college_name: Name of the college
            
        Returns:
            Dictionary with results
        """
        logger.info(f"Processing {college_name}")
        
        results = {
            'college_name': college_name,
            'search_results': [],
            'found_files': [],
            'downloaded_files': [],
            'errors': []
        }
        
        try:
            # Step 1: Google search for CDS files
            potential_urls = self.google_search_cds(college_name)
            results['search_results'] = potential_urls
            
            if not potential_urls:
                logger.warning(f"No CDS URLs found for {college_name}")
                return results
            
            # Step 2: Search each URL for CDS files, prioritizing the first few results
            all_cds_files = []
            for url in potential_urls[:3]:  # Check first 3 Google results
                logger.info(f"Searching {url} for CDS files")
                cds_files = self.find_most_recent_cds_on_page(url)
                all_cds_files.extend(cds_files)
                time.sleep(1)  # Be respectful to the server
            
            # Remove duplicates and sort by year
            unique_files = {}
            for file_info in all_cds_files:
                key = file_info['url']
                if key not in unique_files or file_info['year'] > unique_files[key]['year']:
                    unique_files[key] = file_info
            
            sorted_files = sorted(unique_files.values(), key=lambda x: x['year'], reverse=True)
            results['found_files'] = sorted_files
            
            if not sorted_files:
                logger.warning(f"No CDS files found for {college_name}")
                return results
            
            # Step 3: Download the most recent file (first in sorted list)
            most_recent_file = sorted_files[0]
            logger.info(f"Downloading most recent CDS for {college_name}: {most_recent_file['name']} (Year: {most_recent_file['year']})")
            
            success = self.download_file(most_recent_file, college_name)
            if success:
                results['downloaded_files'].append(most_recent_file)
            
        except Exception as e:
            logger.error(f"Error processing {college_name}: {e}")
            results['errors'].append(str(e))
        
        return results
    
    def process_colleges_batch(self, colleges: List[Dict[str, str]]) -> List[Dict[str, any]]:
        """
        Process multiple colleges
        
        Args:
            colleges: List of dictionaries with 'name' key
            
        Returns:
            List of results for each college
        """
        all_results = []
        
        for college in colleges:
            result = self.process_college(college['name'])
            all_results.append(result)
            
            # Save progress after each college
            self.save_progress(all_results, college['name'])
            
            # Respectful delay between colleges to avoid rate limiting
            logger.info(f"Waiting 5 seconds before processing next college...")
            time.sleep(5)
        
        return all_results

    def extract_year(self, text: str) -> int:
        # Look for various year formats
        patterns = [
            r'20\d{2}',  # Basic year
            r'20\d{2}-20\d{2}',  # Academic year
            r'20\d{2}/\d{2}',  # Year/YY format
        ]
        
        years = []
        for pattern in patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                if '-' in match:
                    years.append(int(match.split('-')[0]))
                elif '/' in match:
                    years.append(int(match.split('/')[0]))
                else:
                    years.append(int(match))
        
        return max(years) if years else 0

    def validate_file(self, filepath: Path) -> bool:
        try:
            # Check file size
            if filepath.stat().st_size < 1000:  # Less than 1KB
                return False
            
            # For PDFs, try to open and validate
            if filepath.suffix.lower() == '.pdf':
                import PyPDF2
                with open(filepath, 'rb') as f:
                    PyPDF2.PdfReader(f)
                
            return True
        except Exception:
            return False

    def save_progress(self, results: List[Dict], college_name: str):
        progress_file = self.download_folder / 'progress.json'
        
        try:
            # Load existing progress
            if progress_file.exists():
                with open(progress_file, 'r') as f:
                    data = json.load(f)
                    existing_results = data.get('results', [])
            else:
                existing_results = []
            
            # Update progress
            for i, result in enumerate(existing_results):
                if result.get('college_name') == college_name:
                    existing_results[i] = results[-1]
                    break
            else:
                existing_results.append(results[-1])
            
            # Save with timestamp
            with open(progress_file, 'w') as f:
                json.dump({
                    'last_updated': datetime.now().isoformat(),
                    'results': existing_results
                }, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving progress: {e}")
            # Create a backup of the results
            backup_file = self.download_folder / f'progress_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
            try:
                with open(backup_file, 'w') as f:
                    json.dump({
                        'last_updated': datetime.now().isoformat(),
                        'results': results
                    }, f, indent=2)
            except Exception as backup_error:
                logger.error(f"Error creating backup: {backup_error}")

def main():
    """
    Example usage of the CDS Downloader
    """
    # Set your Claude API key here or use environment variable
    api_key = os.getenv('CLAUDE_API_KEY')
    if not api_key:
        print("Please set your CLAUDE_API_KEY environment variable")
        return
    
    # Initialize the downloader
    downloader = CDSDownloader(api_key)
    
    # Colleges to process
    colleges = [
        {'name': 'University of Pennsylvania'},
        {'name': 'Carnegie Mellon University'},
        {'name': 'Princeton University'},
        {'name': 'University of Delaware'},
        {'name': 'California Institute of Technology'},
        {'name': 'Massachusetts Institute of Technology'},
        {'name': 'Stanford University'},
        {'name': 'Georgia Institute of Technology'},
        {'name': 'Columbia University'},
        {'name': 'Brown University'},
        {'name': 'University of Michigan'},
        {'name': 'Johns Hopkins University'},
        {'name': 'University of Illinois Urbana-Champaign'},
        {'name': 'Northeastern University'},
        {'name': 'University of Maryland College Park'},
        {'name': 'Rice University'},
        {'name': 'Purdue University'},
        {'name': 'Pennsylvania State University'}
    ]
    
    # Process the colleges
    results = downloader.process_colleges_batch(colleges)
    
    # Print summary
    print("\n" + "="*50)
    print("SUMMARY")
    print("="*50)
    
    total_downloaded = 0
    for result in results:
        print(f"\n{result['college_name']}:")
        print(f"  Search results found: {len(result['search_results'])}")
        print(f"  CDS files found: {len(result['found_files'])}")
        print(f"  Files downloaded: {len(result['downloaded_files'])}")
        if result['downloaded_files']:
            file_info = result['downloaded_files'][0]
            print(f"  Downloaded: {file_info['name']} (Year: {file_info.get('year', 'Unknown')})")
            total_downloaded += 1
        if result['errors']:
            print(f"  Errors: {len(result['errors'])}")
    
    print(f"\nTotal files downloaded: {total_downloaded}")
    print(f"All files saved to: {downloader.download_folder}")

if __name__ == "__main__":
    main()