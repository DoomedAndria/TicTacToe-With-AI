import random


class Tictactoe:

    def __init__(self, ):
        self.table = [[' ' for _ in range(3)] for _ in range(3)]
        self.turn_x = True
        self.game_over = False
        self.p1 = ""
        self.p2 = ""
        self.final_sentence = ""

    def start_game(self):
        self.game_over = False
        self.input_command()
        if not self.game_over:
            self.print_table()
            while True:
                self.make_move(self.p1)
                self.print_table()
                self.check_table()
                if self.game_over:
                    break

                self.make_move(self.p2)
                self.print_table()
                self.check_table()
                if self.game_over:
                    break

            print(self.final_sentence)
            self.__init__()
            self.start_game()

    def input_command(self):
        cmd = input("Input command:")
        try:
            command, p1, p2 = cmd.split()

            if command == "start" and (p1 == "user" or p1 == "easy" or p1 == "medium" or p1 == "hard") \
                    and (p2 == "user" or p2 == "easy" or p2 == "medium" or p2 == "hard"):
                self.p1 = p1
                self.p2 = p2
            else:
                print("Bad parameters!")
                self.input_command()
        except ValueError:
            if cmd == "exit":
                self.game_over = True
            else:
                print("Bad parameters!")
                self.input_command()

    def print_table(self):
        print("---------")
        for i in range(3):
            print("| " + self.table[i][0] + " " +
                  self.table[i][1] + " " +
                  self.table[i][2] + " |")
        print("---------")

    def make_move(self, player):
        if player == "user":
            self.input_coordinates()
        else:
            print("Making move level \"{}\"".format(player))
            self.pc_move(player)

    def input_coordinates(self):
        coordinates = input("Enter the coordinates:")

        try:
            x, y = map(lambda i: int(i) - 1, coordinates.split())

            if x > 2 or x < 0 or y > 2 or y < 0:
                print("Coordinates should be from 1 to 3!")
                self.input_coordinates()
            elif self.table[x][y] != ' ':
                print("This cell is occupied! Choose another one!")
                self.input_coordinates()
            else:
                if self.turn_x:
                    self.table[x][y] = 'X'
                else:
                    self.table[x][y] = 'O'
                self.turn_x = not self.turn_x

        except ValueError:
            print("You should enter numbers!")
            self.input_coordinates()

    def pc_move(self, player):
        if player == "easy":
            self.easy_move()
        elif player == "medium":
            self.medium_move()
        elif player == "hard":
            self.hard_move()

    def easy_move(self):
        x, y = random.randint(0, 2), random.randint(0, 2)
        if self.table[x][y] != ' ':
            self.easy_move()
        else:
            if self.turn_x:
                self.table[x][y] = 'X'
            else:
                self.table[x][y] = 'O'
            self.turn_x = not self.turn_x

    def medium_move(self):
        for i in range(3):
            for j in range(3):
                if self.turn_x:
                    if self.chk_good_move('X', i, j):
                        self.table[i][j] = 'X'
                        self.turn_x = not self.turn_x
                        return
                else:
                    if self.chk_good_move('O', i, j):
                        self.table[i][j] = 'O'
                        self.turn_x = not self.turn_x
                        return
        for i in range(3):
            for j in range(3):
                if self.turn_x:
                    if self.chk_good_move('O', i, j):
                        self.table[i][j] = 'X'
                        self.turn_x = not self.turn_x
                        return
                else:
                    if self.chk_good_move('X', i, j):
                        self.table[i][j] = 'O'
                        self.turn_x = not self.turn_x
                        return
        self.easy_move()

    def hard_move(self):
        best_score = 0
        a = None
        b = None

        if self.turn_x:
            maximizer, minimizer = 'X', 'O'
        else:
            maximizer, minimizer = 'O', 'X'

        for i in range(3):
            for j in range(3):
                if self.table[i][j] == ' ':
                    self.table[i][j] = maximizer
                    score = self.minimax(self.table, False, maximizer, minimizer)
                    self.table[i][j] = ' '
                    if score > best_score:
                        best_score = score
                        a, b = i, j
        self.table[a][b] = maximizer
        self.turn_x = not self.turn_x

    def minimax(self, table, is_maximizing, maximizer, minimizer):
        if self.table_full():
            return 2
        elif self.wins(maximizer):
            return 3
        elif self.wins(minimizer):
            return 1

        if is_maximizing:
            best_score = 0
            for i in range(3):
                for j in range(3):
                    if self.table[i][j] == ' ':
                        self.table[i][j] = maximizer
                        score = self.minimax(table, False, maximizer, minimizer)
                        self.table[i][j] = ' '
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = 4
            for i in range(3):
                for j in range(3):
                    if self.table[i][j] == ' ':
                        self.table[i][j] = minimizer
                        score = self.minimax(table, True, maximizer, minimizer)
                        self.table[i][j] = ' '
                        best_score = min(score, best_score)
            return best_score

    def chk_good_move(self, ch, k, m):
        if self.table[k][m] == ' ':
            # horizontal/vertical
            if self.table[k][(m + 1) % 3] == self.table[k][(m + 2) % 3] \
                    and self.table[k][(m + 1) % 3] == ch \
                    or \
                    self.table[(k + 1) % 3][m] == self.table[(k + 2) % 3][m] \
                    and self.table[(k + 1) % 3][m] == ch:
                return True
            # diagonals
            if k == 0 and m == 0 and self.table[1][1] == self.table[2][2] and self.table[1][1] == ch or \
                    k == 0 and m == 2 and self.table[1][1] == self.table[2][0] and self.table[1][1] == ch or \
                    k == 2 and m == 0 and self.table[1][1] == self.table[0][2] and self.table[1][1] == ch or \
                    k == 2 and m == 2 and self.table[1][1] == self.table[0][0] and self.table[1][1] == ch or \
                    k == 1 and m == 1 and (self.table[0][0] == self.table[2][2] and self.table[0][0] == ch or
                                           self.table[0][2] == self.table[2][0] and self.table[0][2] == ch):
                return True
        return False

    def check_table(self):
        if self.wins('X'):
            self.game_over = True
            self.final_sentence = "X wins"
        elif self.wins('O'):
            self.game_over = True
            self.final_sentence = "O wins"
        elif self.table_full():
            self.game_over = True
            self.final_sentence = "Draw"

    def wins(self, ch):
        for i in range(3):
            if self.table[i][0] == ch and \
                    self.table[i][0] == self.table[i][1] and \
                    self.table[i][1] == self.table[i][2] \
                    or \
                    self.table[0][i] == ch and \
                    self.table[0][i] == self.table[1][i] and \
                    self.table[1][i] == self.table[2][i]:
                return True
        if (self.table[0][0] == self.table[1][1] and self.table[1][1] == self.table[2][2] or
            self.table[0][2] == self.table[1][1] and self.table[1][1] == self.table[2][0]) \
                and self.table[1][1] == ch:
            return True
        return False

    def table_full(self):
        for row in self.table:
            for ch in row:
                if ch == ' ':
                    return False
        return True


game = Tictactoe()
game.start_game()
