from collections import deque

from utils.grid import Grid
from year2019.intcode import IntCode


class Game(Grid):
    SKIP = (".",)
    PLOT = {
        "0": 0,
        "1": 100,
        "2": 200,
        "3": 300,
        "4": 400,
    }
    PLOT_BOX = (24, 42)

    def __init__(self, lines):
        super().__init__(lines)
        self.score = 0
        self.ball = deque([])
        self.paddle = None

    def add_block(self, x, y, tile_id):
        self.grid[(x, y)] = str(tile_id)
        if tile_id == 4:
            if len(self.ball) == 2:
                self.ball.pop()
            self.ball.appendleft((x, y))
        elif tile_id == 3:
            self.paddle = (x, y)

    def set_score(self, value):
        self.score = value

    def get_play(self):
        if len(self.ball) != 2:
            return 0

        bx, by = self.ball[0]
        px, py = self.paddle
        vx = self.ball[0][0] - self.ball[1][0]
        vy = self.ball[0][1] - self.ball[1][1]

        if vy <= 0:
            if bx > px:
                return 1
            elif bx < px:
                return -1
            else:
                return 0
        else:
            target_x = bx + vx * (21 - by)
            if px == target_x:
                return 0
            elif px < target_x:
                return 1
            else:
                return -1

    def add_to_plot(self, plot_grid):
        for text in self.ax.texts:
            text.remove()
        self.ax.text(1, 1, f"{self.score}", fontsize=15, color="yellow")
        x, y = self.ball[0]
        plot_grid[y][x] = 400
        x, y = self.paddle
        plot_grid[y][x] = 300
        return None


def process_input(blob):
    return [int(n) for n in blob.split(",")]


def do_part_1(program):
    intcode = IntCode(
        program, seed=[0], silent=True, seed_only=True, pause_after_output=True
    )
    i = 0
    num_blocks = 0
    intcode.resume()
    while intcode.is_not_done:
        code = intcode.read()
        if i == 2:
            tile_id = code
            if tile_id == 2:
                num_blocks += 1
        i = (i + 1) % 3
        intcode.resume()
    return num_blocks


def do_part_2(program):
    game = Game([])
    intcode = IntCode(
        program, seed=[0], silent=True, seed_only=True, pause_after_output=True
    )
    i = 0
    x = y = None
    intcode.p[0] = 2
    intcode.run()
    while intcode.is_not_done:
        if intcode.waiting_input:
            # provide info/input to intcode
            intcode.add_to_seed(game.get_play())
        else:
            # get info from intcode
            code = intcode.read()
            if i == 0:
                x = code
            elif i == 1:
                y = code
            elif i == 2:
                if (x, y) == (-1, 0):
                    game.set_score(code)
                else:
                    tile_id = code
                    game.add_block(x, y, tile_id)
            i = (i + 1) % 3
        intcode.resume()
    return game.score


def do_visualization(program):
    game = Game([])
    intcode = IntCode(
        program, seed=[0], silent=True, seed_only=True, pause_after_output=True
    )
    i = 0
    x = y = None
    intcode.p[0] = 2
    intcode.run()
    start_plotting = False
    game.initialize_plot()
    while intcode.is_not_done:
        if intcode.waiting_input:
            # provide info/input to intcode
            intcode.add_to_seed(game.get_play())
        else:
            # get info from intcode
            code = intcode.read()
            if i == 0:
                x = code
            elif i == 1:
                y = code
            elif i == 2:
                if (x, y) == (-1, 0):
                    game.set_score(code)
                else:
                    tile_id = code
                    game.add_block(x, y, tile_id)
                if (x, y) == (41, 23):
                    start_plotting = True
            i = (i + 1) % 3
        intcode.resume()
        if start_plotting:
            game.refresh_plot()
    return game.score
