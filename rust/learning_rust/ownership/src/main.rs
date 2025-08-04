fn main() {
    let st1 = dangle();

    println!("{st1}");
}

fn dangle() -> String {
    let mut s = String::from("hi");
    s.push('b');
    s
}
