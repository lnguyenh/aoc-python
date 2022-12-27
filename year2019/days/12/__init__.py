from itertools import combinations

from utils.strings import remove_from_string


class Moon:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.vx = 0
        self.vy = 0
        self.vz = 0

    def apply_velocity(self):
        self.x += self.vx
        self.y += self.vy
        self.z += self.vz

    @property
    def energy(self):
        return sum(map(abs, [self.x, self.y, self.z])) * sum(
            map(abs, [self.vx, self.vy, self.vz])
        )


class Galaxy:
    def __init__(self, lines):
        self.lines = lines
        self.moons = []
        for line in lines:
            x, y, z = line.split(",")
            self.moons.append(Moon(int(x), int(y), int(z)))

    def do_step(self):
        for m1, m2 in combinations(self.moons, 2):
            if m1.x < m2.x:
                m1.vx += 1
                m2.vx -= 1
            elif m1.x > m2.x:
                m1.vx -= 1
                m2.vx += 1
            if m1.y < m2.y:
                m1.vy += 1
                m2.vy -= 1
            elif m1.y > m2.y:
                m1.vy -= 1
                m2.vy += 1
            if m1.z < m2.z:
                m1.vz += 1
                m2.vz -= 1
            elif m1.z > m2.z:
                m1.vz -= 1
                m2.vz += 1
        for m in self.moons:
            m.apply_velocity()
        toto = 1

    def do_n_steps(self, n):
        for _ in range(n):
            self.do_step()

    def get_part_1(self):
        return sum([m.energy for m in self.moons])


def process_input(blob):
    cleaned = remove_from_string(blob, ["<x=", " ", "z=", ">", "y="])
    return cleaned.split("\n")


def do_part_1(lines):
    galaxy = Galaxy(lines)
    galaxy.do_n_steps(1000)
    return galaxy.get_part_1()


def do_part_2(processed_input):
    return "toto"


def do_visualization(processed_input):
    return None
