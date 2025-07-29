fn main() {
    let y = 5;

    println!("another_function(y) = {}", another_function(y));
}

fn another_function(val: isize) -> isize {
    val * 2
}
