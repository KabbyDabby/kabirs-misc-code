use std::collections::HashSet;

fn main() {
    // let input: &str = include_str!("input.txt").trim();
    let input: &str = include_str!("test.txt").trim();
    // let input: &str = include_str!("trivial.txt").trim();
    println!("{}", part2(input));
}

fn part1(input: &str) -> u128 {
    let ranges: Vec<&str> = input.split(",").collect();

    let mut lowers: Vec<&str> = Vec::new();
    let mut uppers: Vec<&str> = Vec::new();

    for s in ranges.iter() {
        let bounds: Vec<&str> = s.split("-").collect();
        lowers.push(bounds.get(0).unwrap());
        uppers.push(bounds.get(1).unwrap());
    }

    let mut sum: u128 = 0;

    let mut seen: HashSet<u128> = HashSet::new();

    for i in 0..lowers.len() {
        let lower_bound = get_lower_half_number(lowers.get(i).unwrap());
        let upper_bound = get_upper_half_number(uppers.get(i).unwrap());

        for j in lower_bound..=upper_bound {
            // println!("{j}");
            let mut s: String = j.to_string();

            s.push_str(&s.clone());
            let num = s.parse::<u128>().expect("failed to parse int");

            if seen.insert(num) {
                sum += num;
            }
        }
    }

    sum
}

fn part2(input: &str) -> u128 {
    let ranges: Vec<&str> = input.split(",").collect();

    let mut lowers: Vec<&str> = Vec::new();
    let mut uppers: Vec<&str> = Vec::new();

    for s in ranges.iter() {
        let bounds: Vec<&str> = s.split("-").collect();
        lowers.push(bounds.get(0).unwrap());
        uppers.push(bounds.get(1).unwrap());
    }

    let mut sum: u128 = 0;

    for i in 0..lowers.len() {
        for j in 2..uppers.get(i).unwrap().len() {
            let lower_bound = get_lower_nth_of_num(lowers.get(i).unwrap(), j);
            let upper_bound = get_upper_nth_of_num(uppers.get(i).unwrap(), j);

            for k in lower_bound..=upper_bound {
                let base: String = k.to_string();

                let s: String = base.repeat(j);

                sum += s.parse::<u128>().expect("failed to parse int");
            }
        }
    }

    sum
}

fn get_lower_nth_of_num(lower: &str, num_pieces: usize) -> u128 {
    let mut ret: String = String::new();
    let chars: Vec<char> = lower.chars().collect();
    // for c in chars.iter() {
    //     // println!(" characters {:?}", c);
    // }
    let len = chars.len();

    if len % num_pieces == 0 {
        let mut pieces: Vec<u128> = Vec::new();

        for i in 0..(num_pieces) {
            let starting_idx = i * (len / num_pieces);
            let mut ending_idx = (i + 1) * (len / num_pieces);

            ending_idx = std::cmp::min(ending_idx, len);

            pieces.push(
                lower[starting_idx..ending_idx]
                    .to_string()
                    .parse::<u128>()
                    .expect(&format!(
                        "failed to parse int; \n{starting_idx}, \n{ending_idx}"
                    )),
            );
        }

        'looop: {
            for i in 1..pieces.len() {
                if pieces.get(i).unwrap() < pieces.get(i - 1).unwrap() {
                    ret = pieces.first().unwrap().to_string();
                    break 'looop;
                } else if pieces.get(i).unwrap() > pieces.get(i - 1).unwrap() {
                    ret = (pieces.first().unwrap() + 1).to_string();
                    break 'looop;
                }
            }

            ret = pieces.first().unwrap().to_string();
        }
    } else {
        ret.push('1');
        for _ in 0..(len / num_pieces) {
            ret.push('0');
        }
    }

    ret.parse::<u128>().expect("Failed to parse int")
}

fn get_upper_nth_of_num(upper: &str, num_pieces: usize) -> u128 {
    let mut ret: String = String::new();
    let chars: Vec<char> = upper.chars().collect();
    // for c in chars.iter() {
    //     // println!(" characters {:?}", c);
    // }

    let len = chars.len();
    if len % num_pieces == 0 {
        let mut pieces: Vec<u128> = Vec::new();

        for i in 0..(num_pieces) {
            let starting_idx = i * (len / num_pieces);
            let mut ending_idx = (i + 1) * (len / num_pieces);

            ending_idx = std::cmp::min(ending_idx, len);

            pieces.push(
                upper[starting_idx..ending_idx]
                    .to_string()
                    .parse::<u128>()
                    .expect("failed to parse int"),
            );
        }

        'looop: {
            for i in 1..pieces.len() {
                if pieces.get(i).unwrap() > pieces.get(i - 1).unwrap() {
                    ret = pieces.first().unwrap().to_string();
                    break 'looop;
                } else if pieces.get(i).unwrap() < pieces.get(i - 1).unwrap() {
                    ret = (pieces.first().unwrap() - 1).to_string();
                    break 'looop;
                }
            }

            ret = pieces.first().unwrap().to_string();
        }
    } else {
        ret.push('1');
        for _ in 0..(len / num_pieces) {
            ret.push('0');
        }
    }

    ret.parse::<u128>().expect("Failed to parse int")
}

fn get_lower_half_number(lower: &str) -> u128 {
    let mut ret: String = String::new();
    let chars: Vec<char> = lower.chars().collect();
    // for c in chars.iter() {
    //     // println!(" characters {:?}", c);
    // }
    let len = chars.len();

    if len % 2 == 0 {
        let first_half: u128 = lower[..(len / 2)]
            .to_string()
            .parse::<u128>()
            .expect("failed to parse int");

        let second_half: u128 = lower[(len / 2)..]
            .to_string()
            .parse::<u128>()
            .expect("failed to parse int");

        if first_half >= second_half {
            ret = first_half.to_string();
        } else {
            ret = (first_half + 1).to_string();
        }
    } else {
        ret.push('1');
        for _ in 0..((len - 1) / 2) {
            ret.push('0');
        }
    }

    ret.parse::<u128>().expect("Failed to parse int")
}

fn get_upper_half_number(upper: &str) -> u128 {
    let mut ret: String = String::new();
    let chars: Vec<char> = upper.chars().collect();
    // for c in chars.iter() {
    //     // println!(" characters {:?}", c);
    // }

    let len = chars.len();
    if len % 2 == 0 {
        let first_half: u128 = upper[..(len / 2)]
            .to_string()
            .parse::<u128>()
            .expect("failed to parse int");

        let second_half: u128 = upper[(len / 2)..]
            .to_string()
            .parse::<u128>()
            .expect("failed to parse int");

        if first_half <= second_half {
            ret = first_half.to_string();
        } else {
            ret = (first_half - 1).to_string();
        }
    } else {
        // println!("upper: {upper}");
        // println!("len: {len}");
        for _ in 0..((len - 1) / 2) {
            ret.push('9');
        }
    }

    ret.parse::<u128>().expect("Failed to parse int")
}
