#[derive(Debug)]
enum IpAddr {
    V4(String),
    V6(String),
}

fn main() {
    let control_hub = IpAddr::V4(String::from("192.168.43.1"));
    let home = IpAddr::V6(String::from("Hi"));

    println!("{control_hub:?}");
    println!("{home:?}");
}
