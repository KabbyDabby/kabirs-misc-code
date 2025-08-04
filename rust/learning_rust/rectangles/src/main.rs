// #[derive(Debug)]
struct Rectangle {
    length: u32,
    width: u32,
}

impl Rectangle {
    fn new(length: u32, width: u32) -> Self {
        Self { length, width }
    }

    fn area(&self) -> u32 {
        self.length * self.width
    }

    fn can_hold(&self, other: &Rectangle) -> bool {
        other.length < self.length && other.width < self.width
    }
}

fn main() {
    let rect1 = Rectangle::new(5, 10);

    let rect2 = Rectangle::new(4, 9);

    println!("The area of the rect1 is {}", rect1.area());
    println!("Can rect2 fit in rect1: {}", rect1.can_hold(&rect2));
}
