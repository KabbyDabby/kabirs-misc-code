fn main() {
    let s = String::from("Hello, World!");

    let fw = first_word(&s);

    println!("{fw}");
}

fn first_word(s: &String) -> &str {
    let bytes = s.as_bytes();

    for (i, &byte) in bytes.iter().enumerate() {
        if byte == b' ' {
            return &s[..i];
        }
    }

    &s[..]
}
