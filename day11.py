test_input = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""

def real_input():
    with open("day11input.txt","r") as f:
        return f.read()


def solve1(galaxy_map: str, adder: int = 1) -> int:
    galaxies = {}
    empty_rows = []
    empty_columns = []
    galaxy_map = [list(i) for i in galaxy_map.split("\n")]
    for r in range(len(galaxy_map)):
        row_empty = True
        for c in range(len(galaxy_map[r])):
            space = galaxy_map[r][c]
            if space == "#": 
                galaxies[(r,c)] = [0,0]
                row_empty = False
        if row_empty:
            empty_rows.append(r)
    for c in range(len(galaxy_map[0])):
        col_empty = True
        for r in range(len(galaxy_map)):
            space = galaxy_map[r][c]
            if space == "#": 
                col_empty = False
        if col_empty:
            empty_columns.append(c)
    for r in empty_rows:
        for gal in galaxies.keys():
            if gal[0] > r:
                galaxies[gal][0]+=adder
    for c in empty_columns:
        for gal in galaxies.keys():
            if gal[1] > c:
                galaxies[gal][1]+=adder
    galaxies_expanded = []
    for gal, adders in galaxies.items():
        galaxies_expanded.append((gal[0]+adders[0],gal[1]+adders[1]))
    total_distance = 0
    for i,gal0 in enumerate(galaxies_expanded[:-1]):
        for gal1 in galaxies_expanded[i+1:]:
            total_distance += abs(gal0[0]-gal1[0]) + abs(gal0[1]-gal1[1])
    return total_distance

if __name__ == "__main__":
    print("Test 1, should be 374")
    print(f"{solve1(test_input) = }")
    print(f"{solve1(real_input()) = }")
    print(f"{solve1(test_input, adder=99) = }")
    print(f"{solve1(real_input(),999999) = }")