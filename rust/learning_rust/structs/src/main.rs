struct User {
    active: bool,
    username: String,
    email: String,
    sign_in_count: u64,
}

fn main() {
    let user1 = User {
        active: true,
        username: String::from("Kubar"),
        email: String::from("email@example.com"),
        sign_in_count: 1,
    };

    println!("{}", user1.username);
}
