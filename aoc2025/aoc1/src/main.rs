const ACTUAL_INPUT: &str = include_str!("input.txt");
const TEST: &str = include_str!("test.txt");

fn main() {
    println!("{}", part_two(ACTUAL_INPUT));
}

fn part_one(input: &str) -> u32 {
    let mut count: u32 = 0;

    let mut curr: i32 = 50;
    let rotations: Vec<&str> = input.split("\n").collect();

    for rotation in rotations.iter() {
        if rotation.is_empty() {
            break;
        }

        let sign: i32 = match &rotation[..1] {
            "L" => -1,
            "R" => 1,
            _ => panic!(),
        };

        let val = &rotation[1..]
            .to_string()
            .parse::<i32>()
            .expect("Failed to parse int");
        curr = (curr + (sign * val)) % 100;

        if curr == 0 {
            count += 1;
        }
    }

    count
}

fn part_two(input: &str) -> u32 {
    let mut count: u32 = 0;

    let mut curr: i32 = 50;
    let rotations: Vec<&str> = input.split("\n").collect();

    for rotation in rotations.iter() {
        if rotation.is_empty() {
            break;
        }

        println!("curr: {curr}, rotation: {rotation}");

        let sign: i32 = match &rotation[..1] {
            "L" => -1,
            "R" => 1,
            _ => panic!(),
        };

        let val = &rotation[1..]
            .to_string()
            .parse::<i32>()
            .expect("Failed to parse int");

        if sign < 0 {
            count += ((val + 100 - curr) / 100) as u32;

            if curr == 0 {
                count -= 1;
            }
        } else {
            count += ((val + curr) / 100) as u32;
        }

        println!("count: {count}");

        curr = (curr + (sign * val)) % 100;

        curr = (curr + 100) % 100
    }

    count
}
