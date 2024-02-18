use crate::aoc2023::utils::read_data_lines;
use log::{debug, error, info};
use regex::Regex;
use std::collections::{HashMap, HashSet};

const DAY: u32 = 3;

fn solve(file_type: String) -> (u32, u32) {
    let lines = read_data_lines(file_type, DAY);
    let re = Regex::new(r"(?P<n>[0-9]+)|(?P<s>[^\.0-9])").unwrap();
    let (mut r, mut c) = (0, 0);
    let mut symbols = HashMap::new();
    let mut nums = HashMap::new();

    for (i, line) in lines.iter().enumerate() {
        debug!("i={:0>3}\t{}", i, line);
        c = line.len();
        r += 1;
        for c in re.captures_iter(line) {
            debug!("{:?}, {:?}, {:?}", c, c.name("n"), c.name("s"));
            match c.name("n") {
                Some(m) => {
                    debug!("Number={:?}", m);
                    let val = (m.start(), m.end(), m.as_str().parse::<u32>().unwrap());
                    for j in m.start()..m.end() {
                        nums.insert((i as i32, j as i32), val);
                    }
                }
                None => (),
            }
            match c.name("s") {
                Some(m) => {
                    debug!("Symbol={:?}", m);
                    symbols.insert((i as i32, m.start() as i32), m.as_str());
                }
                None => (),
            }
        }
    }
    debug!("Rows: {:?}, Cols: {:?}", 0..r, 0..c);
    debug!("nums={:?}", nums);
    debug!("symbols={:?}", symbols);

    let mut symbol_nums = HashMap::new();

    let mut moves: Vec<(i32, i32)> = (-1..=1)
        .flat_map(|x| (-1..=1).map(move |y| (y, x)))
        .filter(|(y, x)| !(x == y && x == &0))
        .collect();
    moves.sort();
    for (y, x) in symbols.keys() {
        for (dy, dx) in &moves {
            let k = (y + dy, x + dx);
            match nums.get(&k) {
                Some(v) => {
                    debug!("(y, x)={:?}, k={:?}, v={:?}", (y, x), k, v);
                    let s = symbol_nums.entry((y, x)).or_insert(HashSet::new());
                    s.insert(v.2);
                }
                None => (),
            }
        }
    }
    debug!("symbol_nums={:?}", symbol_nums);
    let total_part1: u32 = symbol_nums.values().flat_map(|x| x).sum();
    debug!("total={:?}", total_part1);

    let start_products: Vec<_> = symbol_nums
        .iter()
        .filter(|((&y, &x), v)| v.len() == 2 && symbols.get(&(y, x)).unwrap() == &"*")
        .map(|(_, v)| v.iter().copied().reduce(|a, b| a * b).unwrap())
        .collect();
    let total_part2: u32 = start_products.iter().sum();
    debug!("start_products={:?}", start_products);
    debug!("total_part2={:?}", total_part2);

    return (total_part1, total_part2);
}

pub fn part_1(file_type: String) -> u32 {
    info!("Part 1");
    let (total_part1, _) = solve(file_type);
    let result = total_part1;
    info!("Total: {}", result);
    return result;
}

pub fn part_2(file_type: String) -> u32 {
    info!("Part 2");
    let (_, total_part2) = solve(file_type);
    let result = total_part2;

    info!("Total: {}", result);
    return result;
}
