const ITEMS: [&str; 12] = [
    "a partridge in a pear tree",
    "two turtle doves",
    "three French hens",
    "four calling birds",
    "five gold rings",
    "six geese a-laying",
    "seven swans a-swimming",
    "eight maids a-milking",
    "nine ladies dancing",
    "ten lords a-leaping",
    "eleven pipers piping",
    "twelve drummers drumming",
];

const SUFFIXES: [&str; 4] = ["st", "nd", "rd", "th"];

fn main() {
    for i in 1..=12 {
        println!("{}\n", line(i));
    }
}

fn line(day: usize) -> String {
    let mut ret = format!(
        "On the {day}{} day of Christmas, my true love gave to me ",
        SUFFIXES[(day - 1).clamp(0, 3)],
    );
    for i in (0..day).rev() {
        if day != 1 && i == 0 {
            ret += "and ";
        }
        ret += ITEMS[i];
        if i != 0 {
            ret += ", ";
        } else {
            ret += ".";
        }
    }

    ret
}
