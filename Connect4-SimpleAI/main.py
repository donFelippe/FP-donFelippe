import tkinter as tk
import random


class Connect4AI:
    def __init__(self, board, player):
        self.board = board
        self.player = player

    def make_move(self):
        for column in range(self.board.columns):
            if self.board.can_drop_piece(column):
                self.board.drop_piece(column, self.player)
                if self.board.check_win(self.player):
                    self.board.remove_piece(column)
                    return column
                self.board.remove_piece(column)

        while True:
            column = random.randint(0, self.board.columns - 1)
            if self.board.can_drop_piece(column):
                return column


class Connect4Board:
    def __init__(self, rows=6, columns=7):
        self.rows = rows
        self.columns = columns
        self.current_player = 1
        self.game_over = False
        self.ai_enabled = False
        self.ai_player = None

        self.root = tk.Tk()
        self.root.title("Connect 4")

        self.canvas = tk.Canvas(self.root, width=columns * 100, height=rows * 100)
        self.canvas.pack()

        self.grid = [[0 for j in range(columns)] for i in range(rows)]

        self.create_grid()

    def create_grid(self):
        for i in range(self.rows):
            for j in range(self.columns):
                self.canvas.create_rectangle(j * 100, i * 100, (j + 1) * 100, (i + 1) * 100, fill="white")

    def drop_piece(self, column, player):
        for i in range(self.rows - 1, -1, -1):
            if self.grid[i][column] == 0:
                self.grid[i][column] = player
                color = "red" if player == 1 else "yellow"  # Set color based on player
                self.canvas.create_oval(column * 100 + 10, i * 100 + 10, column * 100 + 90, i * 100 + 90, fill=color)
                if self.check_win(player):
                    self.canvas.create_text(350, 300, text="Player {} wins!".format(player), font=("Arial", 30))
                    self.game_over = True
                elif self.check_draw():
                    self.canvas.create_text(350, 300, text="It's a draw!", font=("Arial", 30))
                    self.game_over = True
                else:
                    self.current_player = 3 - self.current_player
                return

    def remove_piece(self, column):
        for i in range(self.rows):
            if self.grid[i][column] != 0:
                self.grid[i][column] = 0
                self.canvas.create_rectangle(column * 100, i * 100, (column + 1) * 100, (i + 1) * 100, fill="white")
                break

    def can_drop_piece(self, column):
        return self.grid[0][column] == 0

    def check_win(self, player):
        for i in range(self.rows):
            for j in range(self.columns):
                if self.grid[i][j] == player:
                    if self.check_direction(i, j, 1, 0, player) or self.check_direction(i, j, 0, 1, player) \
                            or self.check_direction(i, j, 1, 1, player) or self.check_direction(i, j, 1, -1, player):
                        return True
        return False

    def check_direction(self, row, column, delta_row, delta_col, player):
        count = 0
        while row >= 0 and row < self.rows and column >= 0 and column < self.columns and self.grid[row][
            column] == player:
            count += 1
            row += delta_row
            column += delta_col
        return count >= 4

    def check_draw(self):
        return all(self.grid[i][j] != 0 for i in range(self.rows) for j in range(self.columns))

    def ai_move(self):
        if self.ai_player is None:
            self.ai_player = Connect4AI(self, 2)
        column = self.ai_player.make_move()
        self.on_mouse_click_ai(column)

    def run(self):
        self.canvas.bind("<Button-1>", self.on_mouse_click)
        self.root.mainloop()

    def on_mouse_click(self, event):
        if self.game_over:
            return
        column = event.x // 100
        if self.can_drop_piece(column):
            self.drop_piece(column, self.current_player)
            self.current_player = 2  # Set player to 2 after player's move

            if self.ai_enabled and not self.game_over:
                self.ai_move()

    def on_mouse_click_ai(self, column):
        if self.game_over:
            return
        if self.can_drop_piece(column):
            self.drop_piece(column, self.current_player)
            self.current_player = 1  # Set player to 1 after AI's move


if __name__ == "__main__":
    board = Connect4Board()
    board.ai_enabled = True
    board.run()
