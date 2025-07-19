# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a personal code repository containing multiple programming projects across different languages and domains:

- **Java Pokemon Battle Simulator** - A comprehensive Pokemon battle simulation game
- **Python Game Development** - PyGame projects including a historical war simulation game
- **Go ASCII Art Tool** - Pokemon image to ASCII converter
- **Competitive Programming** - Advent of Code solutions and Project Euler problems
- **AI/ML Projects** - Python scripts for data analysis

## Project Structure

### Java Pokemon Project (`java/pokemon_project/`)
- **Main Class**: `PokemonSimulation.java` - Entry point for the Pokemon battle simulator
- **Core Components**:
  - `Pokemon.java` - Pokemon entity with stats, moves, and battle mechanics
  - `PokemonTrainer.java` - Trainer class managing Pokemon teams
  - `Move.java` - Move/attack system with damage calculation
  - `PokemonConsts.java` - Constants for Pokemon data (HP, moves, types)
- **Data Files**: `PokemonData.txt`, `moves.txt` - Pokemon and move definitions
- **Images**: `Pokédex Images/` - PNG files for Pokemon sprites

### Python Projects (`python/`)
- **PyGame Games** (`python/pygame/`):
  - `euro_final.py` - Historical war simulation game with multiple levels
  - `bouncing_ball.py` - Simple physics simulation
- **Competitive Programming**:
  - `Advent of Code 2019/`, `Advent of Code 2023/`, `Advent of Code 2024/` - Annual coding challenges
  - `Project Euler/` - Mathematical programming problems
- **AI/ML** (`python/AI/`):
  - `CDS_Analysis.py` - Data analysis scripts
  - `CDS_Downloader.py` - Data collection utilities

### Go Project (`pokemon_ascii/`)
- **Purpose**: Convert Pokemon images to ASCII art
- **Dependencies**: Uses `ascii-image-converter` library for image processing

## Common Development Tasks

### Running Java Pokemon Simulator
```bash
cd java/pokemon_project
javac *.java
java PokemonSimulation
```

### Running Python Games
```bash
cd python/pygame
python euro_final.py  # Historical war simulation
python bouncing_ball.py  # Physics simulation
```

### Installing Python Dependencies
```bash
pip install -r requirements.txt
```

### Running Go ASCII Converter
```bash
cd pokemon_ascii
go run main.go
```

## Key Dependencies

### Python
- `pygame==2.5.2` - Game development framework
- `numpy==1.24.3` - Numerical computing

### Go
- `ascii-image-converter` - Image to ASCII conversion
- `imaging` - Image processing utilities

### Java
- Standard Java libraries
- File I/O for Pokemon data loading
- Scanner for user input in interactive gameplay

## Architecture Notes

### Pokemon Battle System
- **Turn-based combat** with speed-based turn order
- **Type effectiveness** system for damage calculation
- **Move system** with PP (Power Points) management
- **Trainer management** with team switching mechanics
- **Data-driven design** with external files for Pokemon stats

### PyGame War Simulation
- **Multi-level progression** representing historical warfare evolution
- **Physics-based collision** system with curved paddle mechanics
- **Audio integration** with sound effects for different weapon types
- **State management** for game flow (menu, gameplay, win conditions)

### File Organization
- Each language project is self-contained in its respective directory
- Shared resources (images, data files) are kept within project directories
- Configuration files (go.mod, requirements.txt) define dependencies

## Development Guidelines

- Java projects use standard compilation workflow
- Python projects require virtual environment setup for dependencies
- Go projects use module system for dependency management
- All projects are designed for interactive execution rather than automated testing