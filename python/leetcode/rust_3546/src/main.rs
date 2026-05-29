impl Solution {
    pub fn can_partition_grid(grid: Vec<Vec<i32>>) -> bool {
    let total = {
        let mut inner = 0;
        for row in grid {
            inner += row.iter()::<i32>.sum();
        }
        inner
    };

    if total % 2 == 1 {
        return false;
    }

    let mut running_total = 0;

    for row in grid {
        running_total += row.iter().sum();
        if running_total == total / 2 {
            return true;
        }
    }

    let inverted_grid = {
        let mut ret: Vec<Vec<i32>> = vec![];
        for i in 0..grid.len() {
            for j in 0..grid.get(0).iter().len() {
                ret[j][i] = grid[i][j];
            }
        }

        ret
    };

    running_total = 0;

    for row in inverted_grid {
        running_total += row.iter().sum();
        if running_total == total / 2 {
            return true;
        }
    }

    false
}}
