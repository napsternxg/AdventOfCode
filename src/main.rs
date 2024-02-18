pub mod aoc2023;
use aoc2023::{day01, day02, day03};
use log::info;
use std::env;

fn main() {
    if env::var("RUST_LOG").is_err() {
        env::set_var("RUST_LOG", "info")
    }
    env_logger::init();
    let args: Vec<String> = env::args().map(|x| x.to_string()).collect();
    dbg!(args.clone());
    let (file_type, day) = match args.as_slice() {
        [] | [_] => ("input".to_string(), 1u32),
        [_, day] => ("input".to_string(), day.parse::<u32>().unwrap()),
        [_, day, file_type, ..] => (file_type.to_string(), day.parse::<u32>().unwrap()),
    };
    // let file_type = if args.len() > 1 { &args[1] } else { "input" };
    // let day = if args.len() > 2 { args[2].parse::<i32>().unwrap() } else { 1 };
    match day {
        1 => {
            day01::part_1(file_type.to_string());
            day01::part_2(file_type.to_string());
        }

        2 => {
            day02::part_1(file_type.to_string());
            day02::part_2(file_type.to_string());
        }

        3 => {
            day03::part_1(file_type.to_string());
            day03::part_2(file_type.to_string());
        }
        _ => info!("Invalid day. Please use day between 1 to 25."),
    }
}
