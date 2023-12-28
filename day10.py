# Day 10

def get_test_data():
    return """7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ"""

def get_test2_data():
    return """FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L"""

ENTERABLE_FROM_BELOW = set("7|F")
ENTERABLE_FROM_ABOVE = set("J|L")
ENTERABLE_FROM_LEFT  = set("7-J")
ENTERABLE_FROM_RIGHT = set("L-F")

EXIT_DIRECTIONS = {
    "7":["left","down"],
    "-":["left","right"],
    "J":["left","up"],
    "|":["up","down"],
    "F":["right","down"],
    "L":["right","up"],
    "S":["up","down","left","right"]
}

CHECK_DIRECTIONS = {
    "left": ENTERABLE_FROM_RIGHT,
    "right": ENTERABLE_FROM_LEFT,
    "up": ENTERABLE_FROM_BELOW,
    "down": ENTERABLE_FROM_ABOVE,
}

def get_real_data():
    with open("day10input.txt","r") as f:
        data = f.read()
    return data

class PipeMap:
    def __init__(self, data: str):
        container = [list(l) for l in data.split("\n")]
        extra_container = [["." for e in l] for l in container]
        self._container = container
        self._extra_container = extra_container
        self.start = self.return_start_position()
        self.position = self.start
        self.steps_in_loop = 0

    def return_start_position(self):
        for y,l in enumerate(self._container):
            for x,icon in enumerate(l):
                if icon == "S":
                    return (y,x)
                
    def return_icon(self, yx: tuple[int,int], direction: str):
        y,x = yx
        if direction=="up":
            y -= 1
        if direction == "down":
            y += 1
        if direction == "right":
            x += 1
        if direction == "left":
            x -= 1
        if y < 0 or x < 0 or y >= len(self._container) or x >= len(self._container[0]):
            return ".", (y,x)
        return self._container[y][x], (y,x)
    
    def pprint(self):
        pmap = [[ee for ee in e] for e in self._extra_container]
        # pmap[self.position[0]][self.position[1]] = "$"
        for l in pmap:
            print(''.join(l))

    def flood(self,y,x):
        if y < 0 or x < 0 or y >= len(self._container) or x >= len(self._container[0]):
            self.outer = True
            return
        if self._extra_container[y][x] != ".":
            return
        self._extra_container[y][x] = "X"
        self.flood(y-1,x)
        self.flood(y+1,x)
        self.flood(y,x-1)
        self.flood(y,x+1)

    def count_spaces_inside_loop(self):
        # first, fill out the extra container
        count_pipe = self.return_steps_in_loop()
        # walk it again, assume clockwise, and floodfill "." with "X"
        self.outer = False # if you hit an edge while flood filling, then you are out of loop
        self.position_old = self.start
        self.steps_in_loop = 0
        icon_current, _ = self.return_icon(self.position, None)
        done = False
        while not done:
            self.steps_in_loop += 1
            dirs_to_check = EXIT_DIRECTIONS[icon_current]
            for direction in dirs_to_check:
                icon, new_pos = self.return_icon(self.position,direction)
                if new_pos == self.position_old: 
                    continue
                if new_pos == self.start: 
                    p0 = self.position
                    p1 = new_pos
                    match direction:
                        case "up":
                            self.flood(p0[0],p0[1]-1)
                            self.flood(p1[0],p1[1]-1)
                        case "down":
                            self.flood(p0[0],p0[1]+1)
                            self.flood(p1[0],p1[1]+1)
                        case "right":
                            self.flood(p0[0]-1,p0[1])
                            self.flood(p1[0]-1,p1[1])
                        case "left":
                            self.flood(p0[0]+1,p0[1])
                            self.flood(p1[0]+1,p1[1])
                    self._extra_container[p0[0]][p0[1]] = icon_current
                    done = True
                    break
                check = CHECK_DIRECTIONS[direction]
                if icon in check:
                    p0 = self.position
                    p1 = new_pos
                    match direction:
                        case "up":
                            self.flood(p0[0],p0[1]-1)
                            self.flood(p1[0],p1[1]-1)
                        case "down":
                            self.flood(p0[0],p0[1]+1)
                            self.flood(p1[0],p1[1]+1)
                        case "right":
                            self.flood(p0[0]-1,p0[1])
                            self.flood(p1[0]-1,p1[1])
                        case "left":
                            self.flood(p0[0]+1,p0[1])
                            self.flood(p1[0]+1,p1[1])
                    self._extra_container[p0[0]][p0[1]] = icon_current
                    self.position_old = self.position
                    self.position = new_pos
                    # print(f"{direction = }")
                    icon_current = icon
                    break
        # count Xs
        xcount = 0
        for row in self._extra_container:
            for each in row:
                if each =="X": xcount+=1
        if not self.outer:
            return xcount
        else:
            return len(self._extra_container)*len(self._extra_container[0]) - xcount - count_pipe

    def return_steps_in_loop(self):
        # initial step
        self.position_old = self.start
        self.steps_in_loop = 0
        icon_current, _ = self.return_icon(self.position, None)
        while True:
            self.steps_in_loop += 1
            dirs_to_check = EXIT_DIRECTIONS[icon_current]
            for direction in dirs_to_check:
                icon, new_pos = self.return_icon(self.position,direction)
                if new_pos == self.position_old: 
                    continue
                if new_pos == self.start: 
                    p0 = self.position
                    p1 = new_pos
                    self._extra_container[p0[0]][p0[1]] = icon_current
                    return self.steps_in_loop
                check = CHECK_DIRECTIONS[direction]
                if icon in check:
                    p0 = self.position
                    p1 = new_pos
                    self._extra_container[p0[0]][p0[1]] = icon_current
                    self.position_old = self.position
                    self.position = new_pos
                    # print(f"{direction = }")
                    icon_current = icon
                    break
            # self.pprint()
            # input()

def solve(data):
    # start by finding S, then walk the loop. answer is steps // 2.
    pipemap = PipeMap(data)
    total_steps = pipemap.return_steps_in_loop()
    print(f"{total_steps = }")
    return total_steps//2

def solve2(data):
    pipemap = PipeMap(data)
    # total_steps = pipemap.return_steps_in_loop()
    spaces_in_loop = pipemap.count_spaces_inside_loop()
    pipemap.pprint()
    return spaces_in_loop

if __name__ == "__main__":
    test = get_test_data()
    real = get_real_data()
    # print("Test: Should be 8")
    # print(solve(test))
    test2 = get_test2_data()
    print(f"{solve2(test2) = }")
    print("Test 2: should be 10")
    print()
    print(f"{solve2(real) = }") # 431 was too low
    
    
