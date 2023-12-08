from dataclasses import dataclass

@dataclass
class IRange:
    # class for inclusive ranges
    s: int
    e: int
    collide_yet: bool = False

    def return_overlap_ranges(self, other):
        return_ranges = []
        
        if self.s > other.e or self.e < other.s:
            return_ranges.append(self)
        elif self.s < other.s:
            return_ranges.append(IRange(self.s,other.s-1))
            if self.e <= other.e:
                return_ranges.append(IRange(other.s,self.e))
            else:
                return_ranges.append(IRange(other.s,other.e))
                return_ranges.append(IRange(other.e+1,self.e))
        else:
            if self.e <= other.e:
                return_ranges.append(self)
            else:
                return_ranges.append(IRange(self.s,other.e))
                return_ranges.append(IRange(other.e+1,self.e))
        return return_ranges

    def collide(self,other):
        return self.s <= other.e and other.s <= self.e

    def offset(self, i):
        self.s += i
        self.e += i

    def __str__(self):
        return f"{self.s}  {self.e}"

    def __repr__(self):
        return self.__str__()


def ranges_from_seeds(seeds):
    start_seeds = []
    for i in range(0,len(seeds),2):
        e = seeds[i] + seeds[i+1] - 1
        start_seeds.append(IRange(seeds[i],e))
    return start_seeds

def range_and_offset_from_map(l):
    dst, src, r = [int(each) for each in l.strip().split(" ")]
    e = src + r - 1
    offset = dst - src
    return [IRange(src, e), offset]

def make_seed_map_ranges(instructions_list):
    map_holder = []
    current_holder = []
    for l in instructions_list[2:]:
        if not l:
            map_holder.append(current_holder)
            current_holder = []
        elif l[0].isalpha():
            continue
        elif l[0].isnumeric():
            current_holder.append(range_and_offset_from_map(l))
    return map_holder

def part2_neat(instructions):
    # get seed nums
    # foor each group of instructions, make a mapper function
    instructions_list = instructions.split("\n")
    seeds = [int(s) for s in instructions_list[0].split(":")[1].strip().split(" ")]
    seeds_to_check = ranges_from_seeds(seeds)
    seed_maps_list = make_seed_map_ranges(instructions_list)
    min_list = []
    print(seeds_to_check)
    for m in seed_maps_list:
        seeds_moved = []
        seeds_stay = []
        for mm, offset in m:
            while seeds_to_check:
                s = seeds_to_check.pop()
                new_s_list = s.return_overlap_ranges(mm)
                for ss in new_s_list:
                    if ss.collide(mm):
                        ss.offset(offset)
                        seeds_moved.append(ss)
                    else:
                        seeds_stay.append(ss)
            seeds_to_check = [e for e in seeds_stay]
        seeds_to_check = seeds_stay + seeds_moved
    min_list = [s.s for s in seeds_to_check]
    print(min_list)
    return min(min_list)

test_input = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""

if __name__ == "__main__":
    print(part2_neat(test_input))