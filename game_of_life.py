import tkinter as tk
import random

class GameOfLife:
    def __init__(self, width: int, height: int, cell_size: int):
        self.width = width // cell_size
        self.height = height // cell_size
        self.grid = [[random.choice([0, 1]) for _ in range(self.height)] for _ in range(self.width)]

    def in_grid_bound(self, x: int, y: int) -> bool:
        if x >= len(self.grid) or x < 0:
            return False
        
        if y >= len(self.grid[0]) or y < 0:
            return False
        
        return True

    def get_neighbors(self, pos: tuple[int]) -> int:
        total = 0

        for x_offset in range(-1, 2):
            for y_offset in range(-1, 2):
                x = pos[0] + x_offset
                y = pos[1] + y_offset

                if not self.in_grid_bound(x, y) or (x, y) == pos:
                    continue

                total += self.grid[x][y]

        return total
    
    def next_cell_state(self, current_state: int, neighbors: int) -> int:
        if current_state == 1:
            if neighbors < 2 or neighbors > 3:
                return 0
        
        else:
            if neighbors == 3:
                return 1
            
        return current_state

    def update_grid(self) -> list[list[int]]:
        new_grid = [[cell for cell in row] for row in self.grid]
        for x in range(self.width):
            for y in range(self.height):
                current_cell = self.grid[x][y]
                neighbors = self.get_neighbors((x, y))

                new_grid[x][y] = self.next_cell_state(current_cell, neighbors)

        self.grid = new_grid
        return self.grid


class Screen:
    def __init__(self, width: int, height: int, cell_size: int):
        root = tk.Tk()
        root.title("Conway's Game of Life")

        self.root = root
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.canvas = tk.Canvas(root, width=width, height=height)
        self.canvas.pack()

    def draw_grid(self, grid: list[list[int]]):
        self.canvas.delete("all")

        for x in range(self.width // cell_size):
            for y in range(self.height // cell_size):
                if grid[x][y] == 1:
                    self.canvas.create_rectangle(x * self.cell_size, y * self.cell_size, (x + 1) * self.cell_size, (y + 1) * self.cell_size, fill="black")

def main(screen: Screen, game: GameOfLife):
    new_grid = game.update_grid()
    screen.draw_grid(new_grid)

    screen.root.after(20, main, screen, game)

if __name__ == "__main__":
    width = 1820
    height = 980
    cell_size = 20

    screen = Screen(width, height, cell_size)
    game = GameOfLife(width, height, cell_size)

    main(screen, game)
    screen.root.mainloop()