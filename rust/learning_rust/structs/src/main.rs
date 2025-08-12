struct User {
    active: bool,
    username: String,
    email: String,
    sign_in_count: u64,
}

impl User {
    fn new(active: bool, username: String, email: String, sign_in_count: u64) -> Self {
        Self {
            active,
            username,
            email,
            sign_in_count,
        }
    }
}

fn main() {
    let user1 = User::new(
        false,
        String::from("kubar"),
        String::from("example@example.com"),
        1,
    );

    println!("{}", user1.active);
    println!("{}", user1.username);
    println!("{}", user1.email);
    println!("{}", user1.sign_in_count);
}
