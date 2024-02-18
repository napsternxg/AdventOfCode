use crate::aoc2023::utils::read_data_lines;
use log::{debug, error, info};
use std::cmp;
use std::str::FromStr;
use std::string::ParseError;

const DAY: u32 = 2;

#[derive(Debug, Clone, Copy, Default)]
struct Sample {
    red: u32,
    blue: u32,
    green: u32,
}

impl Sample {
    pub fn update(&mut self, color: &str, n: u32) {
        match color {
            "red" => self.red += n,
            "blue" => self.blue += n,
            "green" => self.green += n,
            _ => error!("Unparsable color: {}", color),
        }
    }

    pub fn is_valid_sample(&self, other: &Self) -> bool {
        return (other.red <= self.red && other.green <= self.green && other.blue <= self.blue);
    }

    pub fn update_max(&mut self, other: &Self) {
        self.red = cmp::max(self.red, other.red);
        self.blue = cmp::max(self.blue, other.blue);
        self.green = cmp::max(self.green, other.green);
    }

    pub fn power(&self) -> u32 {
        return self.red * self.green * self.blue;
    }
}

impl FromStr for Sample {
    type Err = ParseError;
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let parts: Vec<String> = s.split(", ").map(str::to_string).collect();
        let mut sample = Sample {
            red: 0,
            blue: 0,
            green: 0,
        };
        for part in parts {
            let color_parts: Vec<String> = part.split(" ").map(str::to_string).collect();
            // debug!("color_parts: {:?}", color_parts);
            let n = color_parts[0].parse::<u32>().unwrap();
            let color = &color_parts[1];
            sample.update(&color, n);
        }
        Ok(sample)
    }
}

fn parse_line(line: String) -> (u32, Vec<Sample>) {
    let parts: Vec<String> = line.split(": ").map(str::to_string).collect();
    let gid = parts[0]
        .split("Game ")
        .last()
        .unwrap()
        .parse::<u32>()
        .unwrap();
    let sample_strings: Vec<String> = parts[1].split("; ").map(str::to_string).collect();
    let samples: Vec<Sample> = sample_strings
        .iter()
        .map(|x| Sample::from_str(x).expect(format!("Sample invalid for x: {}", x).as_str()))
        .collect();

    // for sample_str in sample_strings.iter() {
    //     let sample = Sample::from_str(sample_str).expect(format!("Sample invalid for x: {}", sample_str).as_str());
    // }
    return (gid, samples);
}

fn is_valid_game(samples: Vec<Sample>, &global_sample: &Sample) -> bool {
    for is_valid in samples.iter().map(|x| global_sample.is_valid_sample(x)) {
        if !is_valid {
            return false;
        }
    }
    return true;
}

fn get_min_sample(samples: Vec<Sample>) -> Sample {
    let mut min_sample = Sample {
        red: 0,
        blue: 0,
        green: 0,
    };
    for sample in samples.iter() {
        min_sample.update_max(sample);
    }
    return min_sample;
}

pub fn part_1(file_type: String) -> u32 {
    info!("Part 1");
    let lines = read_data_lines(file_type, DAY);
    let mut result = 0;
    let global_sample = Sample {
        red: 12,
        blue: 14,
        green: 13,
    };
    for line in lines {
        let (gid, samples) = parse_line(line);
        debug!("Game {}:", gid);
        debug!("{:?}", samples);
        if is_valid_game(samples, &global_sample) {
            result += gid;
        }
    }

    info!("Total: {}", result);
    return result;
}

pub fn part_2(file_type: String) -> u32 {
    info!("Part 2");
    let lines = read_data_lines(file_type, DAY);
    let mut result = 0;

    for line in lines {
        let (gid, samples) = parse_line(line);
        debug!("Game {}:", gid);
        debug!("{:?}", samples);
        result += get_min_sample(samples).power();
    }

    info!("Total: {}", result);
    return result;
}
