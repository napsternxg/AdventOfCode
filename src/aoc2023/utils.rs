use log::info;
use std::fs;

pub fn read_data(file_type: String, day: u32) -> String {
    let file_path = format!("./data/2023/{:0>2}/{}.txt", day, file_type);
    info!("Reading file {}", file_path);

    let data = fs::read_to_string(file_path).expect("");
    return data;
}

pub fn read_data_lines(file_type: String, day: u32) -> Vec<String> {
    let data = read_data(file_type, day);
    let lines = data.split("\n").map(str::to_string).collect();
    return lines;
}
