def greet():
    print("  ―――――――――――")
    print(" | Приветствуем вас |")
    print(" |     в игре       |")
    print(" | крестики-нолики  |")
    print(" |   (づ｡◕‿‿◕｡)づ    |")
    print("  ―――――――――――")
    print("  формат ввода: x y ")
    print("  x - номер строки  ")
    print("  y - номер столбца ")


def show():
    print()
    print(f"    │ 0 │ 1 │ 2 │")
    print("  ―――――――――")
    for i, row in enumerate(field):
        row_str = f"  {i} │ {' │ '.join(row)} │ "
        print(row_str)
        print("  ―――――――――")


def ask():
    while True:
        cord = input("  Ваш ход: ").split()

        if len(cord) != 2:
            print(" Введите две координаты!!! (－‸ლ)")
            continue
        x, y = cord

        if not (x.isdigit()) or not (y.isdigit()):
            print("Введите числа !!! (╮°-°)╮┳━━┳ (╯°□°)╯ ┻━━┻")
            continue

        x, y = int(x), int(y)

        if 0 > x or x > 2 or 0 > y or y > 2:
            print(" Координаты вне диапазона!!! 凸(￣ヘ￣)")
            continue

        if field[x][y] != " ":
            print(" Клетка занята!!! (╥﹏╥)")
            continue

        return x, y


def check_win():
    win_cord = (
        ((0, 0), (0, 1), (0, 2)),
        ((1, 0), (1, 1), (1, 2)),
        ((2, 0), (2, 1), (2, 2)),
        ((0, 2), (1, 1), (2, 0)),
        ((0, 0), (1, 1), (2, 2)),
        ((0, 0), (1, 0), (2, 0)),
        ((0, 1), (1, 1), (2, 1)),
        ((0, 2), (1, 2), (2, 2))
    )
    for cord in win_cord:
        symbols = []
        for c in cord:
            symbols.append(field[c[0]][c[1]])
        if symbols == ["X", "X", "X"]:
            show()
            print("  Выиграл X !!!  ＼(＾▽＾)／ ")
            return True
        if symbols == ["O", "O", "O"]:
            show()
            print("  Выиграл O !!!  ＼(＾▽＾)／ ")
            return True
    return False


def new_game():
    while True:
        ans = input("  Cыграем еще раз?  Y - да, N - нет: ")
        if ans.upper() == "Y":
            return True
        elif ans.upper() == "N":
            print("  Пакеда! (>﹏<) ")
            return False
        else:
            print("  Y - да, N - нет: ")


greet()
field = [[" "] * 3 for i in range(3)]
motion = 0

while True:
    motion += 1

    show()

    if motion % 2 == 1:
        print("  Ходит крестик X ")
    else:
        print("  Ходит нолик ◯ ")

    x, y = ask()

    if motion % 2 == 1:
        field[x][y] = "X"
    else:
        field[x][y] = "O"
    if check_win():
        if new_game():
            field = [[" "] * 3 for i in range(3)]
            motion = 0
            show()
            continue
        else:
            break

    if motion == 9:
        print("  Ничья ¯\_(ツ)_/¯")
        if new_game():
            field = [[" "] * 3 for i in range(3)]
            motion = 0
            show()
            continue
        else:
            break
