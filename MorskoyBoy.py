from random import randint


class BoardException(Exception):
    pass


class OutException(BoardException):
    def __str__(self):
        return "(ಠ_ಠ) Внимание!!! попытка выстрела за пределы поля!!!"


class UsedDotException(BoardException):
    def __str__(self):
        return "(；･ω･)ア По этим координатам уже был открыт огонь!!!"


class BoardWrongShipException(BoardException):
    pass


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"Dot({self.x}, {self.y})"


class Ship:
    def __init__(self, bow, ln, o):
        self.bow = bow
        self.ln = ln
        self.o = o
        self.lives = ln

    @property
    def dots(self):
        ship_dots_lst = []
        for i in range(self.ln):
            cur_x = self.bow.x
            cur_y = self.bow.y

            if self.o == 0:
                cur_x += i

            elif self.o == 1:
                cur_y += i

            ship_dots_lst.append(Dot(cur_x, cur_y))

        return ship_dots_lst

    def shooten(self, shot):
        return shot in self.dots


class Board:
    def __init__(self, hid=False, size=6):
        self.size = size
        self.hid = hid

        self.count = 0

        self.field = [["□"] * size for _ in range(size)]

        self.busy = []
        self.ships = []

    def __str__(self):
        res = ""
        res += "  │ 1 │ 2 │ 3 │ 4 │ 5 │ 6 │"
        for i, row in enumerate(self.field):
            res += f"\n{i + 1} │ " + " │ ".join(row) + " │"

        if self.hid:
            res = res.replace("■", "□")
        return res

    def out(self, d):
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    def contour(self, ship, verb=False):
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not (self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = "•"
                    self.busy.append(cur)

    def add_ship(self, ship):
        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise BoardWrongShipException()
        for d in ship.dots:
            self.field[d.x][d.y] = "■"
            self.busy.append(d)

        self.ships.append(ship)
        self.contour(ship)

    def shot(self, d):
        if self.out(d):
            raise OutException()

        if d in self.busy:
            raise UsedDotException()

        self.busy.append(d)

        for ship in self.ships:
            if d in ship.dots:
                ship.lives -= 1
                self.field[d.x][d.y] = "X"
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, verb=True)
                    print('Корабль "ПОМЕР" †')
                    return False
                else:
                    print("Ранен! Но не убит !!! (@_@)")
                    return True

        self.field[d.x][d.y] = "•"
        print("Мимо !!! (－‸ლ)")
        return False

    def begin(self):
        self.busy = []

    def defeat(self):
        return self.count == len(self.ships)


class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)


class AI(Player):
    def ask(self):
        d = Dot(randint(0, 5), randint(0, 5))
        print(f"Ход Электроника (≧◡≦) {d.x + 1} {d.y + 1} ")
        return d


class User(Player):
    def ask(self):
        while True:
            cords = input("Твой ход, Кожаный ! (ಠ_ಠ) ").split()

            if len(cords) != 2:
                print("Введите 2 координаты ! (╯°益°)╯ ")
                continue

            x, y = cords

            if not (x.isdigit()) or not (y.isdigit()):
                print("Кожаный, введи ЧИСЛА !!!! (╯°□°)╯ ┻━━┻ ")
                continue

            x, y = int(x), int(y)

            return Dot(x - 1, y - 1)


class Game:
    def __init__(self, size=6):
        self.lens = [3, 2, 2, 1, 1, 1, 1]
        self.size = size
        pl = self.random_board()
        co = self.random_board()
        co.hid = True

        self.ai = AI(co, pl)
        self.us = User(pl, co)

    def try_board(self):
        board = Board(size=self.size)
        attempts = 0
        for ln in self.lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), ln, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    def random_board(self):
        board = None
        while board is None:
            board = self.try_board()
        return board

    @staticmethod
    def greet():
        print("-" * 27)
        print("      Приветствуем вас  ")
        print("          в игре       ")
        print("        морской бой    ")
        print("-" * 27)
        print("      формат ввода: x y ")
        print("      x - номер строки  ")
        print("      y - номер столбца ")

    def print_boards(self):
        print("-" * 27)
        print("     Доска пользователя")
        print(self.us.board)
        print("-" * 27)
        print("     Доска электроника")
        print(self.ai.board)
        print("-" * 27)

    def loop(self):
        num = 0
        while True:
            self.print_boards()
            if num % 2 == 0:
                print("Ходит пользователь!")
                repeat = self.us.move()
            else:
                print("Ходит электроник!")
                repeat = self.ai.move()
            if repeat:
                num -= 1

            if self.ai.board.defeat():
                self.print_boards()
                print("-" * 27)
                print("Пользователь выиграл!")
                break

            if self.ai.board.defeat():
                self.print_boards()
                print("-" * 27)
                print("Электроник выиграл!")
                break
            num -= 1

    def start(self):
        self.greet()
        self.loop()


g = Game()
g.start()
