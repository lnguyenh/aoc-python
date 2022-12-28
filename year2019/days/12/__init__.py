from itertools import combinations
from math import lcm

from utils.strings import remove_from_string


class Moon:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.vx = 0
        self.vy = 0
        self.vz = 0
        self.x0 = x
        self.y0 = y
        self.z0 = z

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

    def do_n_steps(self, n):
        for _ in range(n):
            self.do_step()

    def get_part_1(self):
        return sum([m.energy for m in self.moons])

    def get_part_2(self):
        a = None
        b = None
        c = None
        i = 0
        while True:
            self.do_step()
            i = i + 1
            if all([m.vx == 0 for m in self.moons]):
                if all([m.x == m.x0 for m in self.moons]):
                    if a is None:
                        a = i
            if all([m.vy == 0 for m in self.moons]):
                if all([m.y == m.y0 for m in self.moons]):
                    if b is None:
                        b = i
            if all([m.vz == 0 for m in self.moons]):
                if all([m.z == m.z0 for m in self.moons]):
                    if c is None:
                        c = i
            if a is not None and b is not None and c is not None:
                break

        return lcm(a, b, c)


def process_input(blob):
    cleaned = remove_from_string(blob, ["<x=", " ", "z=", ">", "y="])
    return cleaned.split("\n")


def do_part_1(lines):
    galaxy = Galaxy(lines)
    galaxy.do_n_steps(1000)
    return galaxy.get_part_1()


def do_part_2(lines):
    galaxy = Galaxy(lines)
    return galaxy.get_part_2()


def do_visualization(processed_input):
    return None
