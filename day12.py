from itertools import combinations

test_input = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""

def real_input():
    with open("day12real.txt","r") as f:
        return f.read()

def solve1(instructions: str) -> int:
    rows = instructions.split("\n")
    total_configs = 0
    for r in rows:
        left,right      = r.split(" ")
        right           = tuple([int(e) for e in right.split(",")])
        total_broke_row = sum(right)
        known_row       = left.count("#")
        guesses         = total_broke_row - known_row
        if guesses == 0: 
            total_configs += 1
            continue
        questions = [i for i,v in enumerate(left) if v == "?"]
        options   = list(combinations(questions,guesses))
        for op in options:
            left_list = list(left)
            for o in op:
                left_list[o] = "#"
            left_tuple = []
            start_count = 0
            for e in left_list:
                if e=="#":
                    start_count+=1
                else:
                    if start_count > 0:
                        left_tuple.append(start_count)
                    start_count = 0
            if start_count > 0:
                left_tuple.append(start_count)
            left_tuple = tuple(left_tuple)
            if left_tuple == right:
                total_configs+=1
    return total_configs


if __name__ == "__main__":
    print("Test is 21")
    print(f"{solve1(test_input) = }")
    print(f"{solve1(real_input()) = }")