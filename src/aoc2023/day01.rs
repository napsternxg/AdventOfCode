use crate::aoc2023::utils::read_data_lines;
use aho_corasick::AhoCorasick;
use log::{debug, info};

const DAY: u32 = 1;

pub fn part_1(file_type: String) -> u32 {
    info!("Part 1");
    // let data = read_data(file_type, DAY);
    // let lines = data.split("\n");
    let lines = read_data_lines(file_type, DAY);
    let mut total = 0;
    for line in lines {
        // debug!("{}", line);
        let mut nums = Vec::new();

        for c in line.chars() {
            if c.is_digit(10) {
                // debug!("{}", c);
                nums.push(c.to_digit(10).unwrap());
            }
        }
        if nums.len() < 1 {
            continue;
        }
        let num = nums[0] * 10 + nums[nums.len() - 1];
        total += num;
        // debug!("");
        // debug!("{:?} -> {}", nums, num);
    }
    info!("Total: {}", total);
    return total;
}

pub fn part_2(file_type: String) -> u32 {
    info!("Part 2");
    let patterns = &[
        "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", // 0..8
        "1", "2", "3", "4", "5", "6", "7", "8", "9",
    ];

    let ac = AhoCorasick::builder()
        .ascii_case_insensitive(true)
        .build(patterns)
        .unwrap();
    let lines = read_data_lines(file_type, DAY);
    let mut total = 0;
    for line in lines {
        // debug!("{}", line);
        let mut nums = Vec::new();
        for mat in ac.find_overlapping_iter(&line) {
            // debug!("{:?}, {}, {}, {}", mat.pattern(), mat.start(), mat.end(), &line[mat.start()..mat.end()]);
            // let i = mat.pattern().as_u32();
            // nums.push(if i < 9 { i + 1 } else { i - 9 + 1 }); // Use offset of 9
            match mat.pattern().as_u32() {
                i if i < 9 => nums.push(i + 1),
                i => nums.push(i - 9 + 1),
            }
        }
        if nums.len() < 1 {
            continue;
        }
        let num = nums[0] * 10 + nums[nums.len() - 1];
        total += num;
        // debug!("");
        // debug!("{:?} -> {}", nums, num);
    }
    info!("Total: {}", total);
    return total;
}
