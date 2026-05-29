use std::{
    fs::{self, File},
    io::{self, Read},
};

fn main() {
    let file_result = File::open("hello.txt").expect("problem reading file");
}

fn get_username_from_file() -> Result<String, io::Error> {
    fs::read_to_string("hello.txt")
}
