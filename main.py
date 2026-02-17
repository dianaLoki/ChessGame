class Figure:
    """Базовый класс для шахматных и шашечных фигур"""

    def __init__(self, color, position, kill=False):
        self.color = color
        self.position = position
        self.kill = kill

    def get_possible_moves(self):
        raise NotImplementedError("Метод должен быть переопределен в дочернем классе")


class CheckersFigure(Figure):
    """Фигура для игры в шашки"""

    def __str__(self):
        return 'O' if self.color == 'white' else 'o'

    def get_possible_moves(self):
        possible_moves = []
        x, y = self.position
        if self.color == 'white':
            possible_moves.append((x - 1, y + 1))
            possible_moves.append((x - 1, y - 1))
        else:
            possible_moves.append((x + 1, y + 1))
            possible_moves.append((x + 1, y - 1))
        return possible_moves


class Ghost(Figure):
    """Фигура 'Призрак' - ходит как ладья"""

    def __str__(self):
        return 'G' if self.color == 'white' else 'g'

    def get_possible_moves(self):
        x, y = self.position
        moves = []
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            for i in range(1, 8):
                nx, ny = x + dx * i, y + dy * i
                if 0 <= nx < 8 and 0 <= ny < 8:
                    moves.append((nx, ny))
                else:
                    break
        return moves


class Pawn(Figure):
    """Шахматная пешка"""

    def __str__(self):
        return 'P' if self.color == 'white' else 'p'

    def get_possible_moves(self):
        possible_moves = []
        x, y = self.position

        # Обычный ход вперед
        if self.color == 'white':
            if x - 1 >= 0:
                possible_moves.append((x - 1, y))
        else:
            if x + 1 < 8:
                possible_moves.append((x + 1, y))

        # Ход на две клетки с начальной позиции
        if x == 6 and self.color == 'white':
            possible_moves.append((x - 2, y))
        elif x == 1 and self.color == 'black':
            possible_moves.append((x + 2, y))

        # Ходы для взятия фигур
        if self.color == 'white':
            if x - 1 >= 0 and y - 1 >= 0:
                possible_moves.append((x - 1, y - 1))
            if x - 1 >= 0 and y + 1 < 8:
                possible_moves.append((x - 1, y + 1))
        else:
            if x + 1 < 8 and y - 1 >= 0:
                possible_moves.append((x + 1, y - 1))
            if x + 1 < 8 and y + 1 < 8:
                possible_moves.append((x + 1, y + 1))

        # Фильтруем ходы за пределами доски
        valid_moves = []
        for move in possible_moves:
            if 0 <= move[0] < 8 and 0 <= move[1] < 8:
                valid_moves.append(move)

        return valid_moves


class Rook(Figure):
    """Шахматная ладья"""

    def __str__(self):
        return 'R' if self.color == 'white' else 'r'

    def get_possible_moves(self):
        possible_moves = []
        x, y = self.position
        for i in range(8):
            if i != x:
                possible_moves.append((i, y))
            if i != y:
                possible_moves.append((x, i))
        return possible_moves


class Knight(Figure):
    """Шахматный конь"""

    def __str__(self):
        return 'N' if self.color == 'white' else 'n'

    def get_possible_moves(self):
        x, y = self.position
        possible_moves = [
            (x + 1, y + 2), (x + 2, y + 1), (x + 1, y - 2), (x + 2, y - 1),
            (x - 1, y + 2), (x - 2, y + 1), (x - 2, y - 1), (x - 1, y - 2)
        ]
        return possible_moves


class Bishop(Figure):
    """Шахматный слон"""

    def __str__(self):
        return 'B' if self.color == 'white' else 'b'

    def get_possible_moves(self):
        possible_moves = []
        x, y = self.position
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dx, dy in directions:
            step = 1
            while True:
                new_x, new_y = x + dx * step, y + dy * step
                if 0 <= new_x < 8 and 0 <= new_y < 8:
                    possible_moves.append((new_x, new_y))
                else:
                    break
                step += 1
        return possible_moves


class Queen(Figure):
    """Шахматный ферзь"""

    def __str__(self):
        return 'Q' if self.color == 'white' else 'q'

    def get_possible_moves(self):
        possible_moves = []
        x, y = self.position

        # Ходы как ладья
        for i in range(8):
            if i != x:
                possible_moves.append((i, y))
            if i != y:
                possible_moves.append((x, i))

        # Ходы как слон
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dx, dy in directions:
            step = 1
            while True:
                new_x, new_y = x + dx * step, y + dy * step
                if 0 <= new_x < 8 and 0 <= new_y < 8:
                    possible_moves.append((new_x, new_y))
                else:
                    break
                step += 1

        return possible_moves


class King(Figure):
    """Шахматный король"""

    def __str__(self):
        return 'K' if self.color == 'white' else 'k'

    def get_possible_moves(self):
        x, y = self.position
        possible_moves = [
            (x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1),
            (x + 1, y + 1), (x - 1, y - 1), (x + 1, y - 1), (x - 1, y + 1)
        ]
        return possible_moves


class Snake(King):
    """Фигура 'Змея' - ходит как король"""

    def __str__(self):
        return 'S' if self.color == 'white' else 's'


class Board:
    """Игровая доска для шахмат"""
    letters = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8}
    numbers = ['1', '2', '3', '4', '5', '6', '7', '8']

    def __init__(self):
        self.field = [[None] * 8 for _ in range(8)]
        self.history = []
        self.setup_board()
        self.save_state()

    def setup_board(self):
        """Начальная расстановка фигур"""
        for col in range(8):
            self.field[1][col] = Pawn("black", (1, col))
            self.field[6][col] = Pawn("white", (6, col))

        back_row = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for col, piece_class in enumerate(back_row):
            self.field[0][col] = piece_class("black", (0, col))
            self.field[7][col] = piece_class("white", (7, col))

    def display_current_board(self):
        """Показывает доску в консоли"""
        print('\nТекущее состояние поля:\n')
        print('     ' + ' '.join([key for key in self.letters.keys()]), end='\n\n')
        for row in range(8):
            row_str = ' '.join(str(piece) if piece else '.' for piece in self.field[row])
            print(self.numbers[row] + '    ' + row_str + '    ' + self.numbers[row])
        print()
        print('     ' + ' '.join([key for key in self.letters.keys()]))
        print()

    def save_state(self):
        """Сохраняет состояние доски для отмены хода"""
        board_copy = [row.copy() for row in self.field]
        self.history.append(board_copy)

    def undo_move(self):
        """Отменяет последний ход"""
        if len(self.history) > 1:
            self.history.pop()
            self.field = self.history[-1]
            print("Ход откатан.")
        else:
            print("Нет ходов для отката.")

    def is_path_clear(self, a1, b1, a2, b2):
        """Проверяет, свободен ли путь между клетками"""
        if a1 == a2:  # Горизонталь
            for col in range(min(b1, b2) + 1, max(b1, b2)):
                if self.field[a1][col] is not None:
                    return False
            return True

        elif b1 == b2:  # Вертикаль
            for row in range(min(a1, a2) + 1, max(a1, a2)):
                if self.field[row][b1] is not None:
                    return False
            return True

        elif abs(a1 - a2) == abs(b1 - b2):  # Диагональ
            row_step = 1 if a2 > a1 else -1
            col_step = 1 if b2 > b1 else -1
            row, col = a1 + row_step, b1 + col_step
            while (row, col) != (a2, b2):
                if self.field[row][col] is not None:
                    return False
                row += row_step
                col += col_step
            return True

        return True  # Для коня и других фигур, которые могут перепрыгивать

    def check_move(self, step1, step2):
        """Проверяет, можно ли сделать такой ход"""
        a1, b1 = step1
        a2, b2 = step2
        figure = self.field[a1][b1]
        target = self.field[a2][b2]

        if figure is None:
            return False

        # Проверяем, что ходим своей фигурой
        if target is not None and target.color == figure.color:
            return False

        possible_moves = figure.get_possible_moves()

        # Для пешки проверяем особые правила взятия
        if isinstance(figure, Pawn) and target is not None:
            # Если бьем фигуру, разрешаем диагональные ходы
            if abs(b2 - b1) == 1 and abs(a2 - a1) == 1:
                return True

        if (a2, b2) not in possible_moves:
            return False

        # Для коня и призрака путь не проверяем
        if isinstance(figure, (Knight, Ghost)):
            return True

        # Для остальных проверяем, свободен ли путь
        return self.is_path_clear(a1, b1, a2, b2)

    def if_rock_possible(self, pl_color):
        """Проверяет, можно ли сделать рокировку"""
        if pl_color == 'white':
            return (isinstance(self.field[0][4], King) and
                    isinstance(self.field[0][7], Rook) and
                    self.field[0][4].color == pl_color and
                    self.field[0][7].color == pl_color and
                    self.is_path_clear(0, 4, 0, 7))
        else:
            return (isinstance(self.field[7][4], King) and
                    isinstance(self.field[7][7], Rook) and
                    self.field[7][4].color == pl_color and
                    self.field[7][7].color == pl_color and
                    self.is_path_clear(7, 4, 7, 7))

    def rock(self, pl_color):
        """Делает рокировку"""
        if pl_color == 'white':
            self.field[0][6] = self.field[0][4]
            self.field[0][4] = None
            self.field[0][5] = self.field[0][7]
            self.field[0][7] = None
        else:
            self.field[7][6] = self.field[7][4]
            self.field[7][4] = None
            self.field[7][5] = self.field[7][7]
            self.field[7][7] = None

    def is_game_over(self):
        """Проверяет, закончилась ли игра"""
        # Упрощенная проверка - ищем королей
        white_king_exists = False
        black_king_exists = False

        for row in range(8):
            for col in range(8):
                piece = self.field[row][col]
                if isinstance(piece, King):
                    if piece.color == 'white':
                        white_king_exists = True
                    else:
                        black_king_exists = True

        return not (white_king_exists and black_king_exists)

    def make_move(self, step1, step2):
        """Выполняет ход"""
        a1, b1 = step1
        a2, b2 = step2
        figure = self.field[a1][b1]

        # Если бьем фигуру
        if self.field[a2][b2] is not None:
            print(f'\nИгрок бьет фигуру противника')
            if isinstance(figure, Snake):
                figure.kill = True

        self.field[a2][b2] = figure
        figure.position = (a2, b2)
        self.field[a1][b1] = None
        self.save_state()


class CheckersBoard(Board):
    """Игровая доска для шашек"""

    def __init__(self):
        super().__init__()

    def setup_board(self):
        """Начальная расстановка шашек"""
        for col in range(8):
            # Черные шашки
            if col % 2 == 0:
                self.field[0][col] = CheckersFigure("black", (0, col))
                self.field[2][col] = CheckersFigure("black", (2, col))
            else:
                self.field[1][col] = CheckersFigure("black", (1, col))

            # Белые шашки
            if col % 2 == 1:
                self.field[5][col] = CheckersFigure("white", (5, col))
                self.field[7][col] = CheckersFigure("white", (7, col))
            else:
                self.field[6][col] = CheckersFigure("white", (6, col))

    def check_move(self, step1, step2):
        """Проверяет ход в шашках"""
        a1, b1 = step1
        a2, b2 = step2
        figure = self.field[a1][b1]

        if figure is None or not isinstance(figure, CheckersFigure):
            return False

        # Проверяем, что ходим на пустую клетку
        if self.field[a2][b2] is not None:
            return False

        possible_moves = figure.get_possible_moves()

        # Обычный ход
        if (a2, b2) in possible_moves and self.is_path_clear(a1, b1, a2, b2):
            return True

        # Ход со взятием
        if abs(a2 - a1) == 2 and abs(b2 - b1) == 2:
            mid_x = (a1 + a2) // 2
            mid_y = (b1 + b2) // 2
            mid_figure = self.field[mid_x][mid_y]
            # Проверяем, что между ними есть вражеская фигура
            if mid_figure is not None and mid_figure.color != figure.color:
                return True

        return False

    def make_move(self, step1, step2):
        """Выполняет ход в шашках"""
        a1, b1 = step1
        a2, b2 = step2
        figure = self.field[a1][b1]

        # Проверяем, было ли взятие
        if abs(a2 - a1) == 2 and abs(b2 - b1) == 2:
            mid_x = (a1 + a2) // 2
            mid_y = (b1 + b2) // 2
            print(f'\nИгрок бьет фигуру противника')
            self.field[mid_x][mid_y] = None
            figure.kill = True

        self.field[a2][b2] = figure
        figure.position = (a2, b2)
        self.field[a1][b1] = None

        # Превращение в дамку
        if (figure.color == 'white' and a2 == 0) or (figure.color == 'black' and a2 == 7):
            print(f'\nФигура {figure.color} стала дамкой!')

    def is_game_over(self):
        """Проверяет, закончилась ли игра в шашки"""
        white_exists = False
        black_exists = False

        for row in range(8):
            for col in range(8):
                figure = self.field[row][col]
                if isinstance(figure, CheckersFigure):
                    if figure.color == 'white':
                        white_exists = True
                    else:
                        black_exists = True

        return not (white_exists and black_exists)


class ExtendedBoard(Board):
    """Расширенная доска с новыми фигурами"""

    def __init__(self):
        super().__init__()

    def setup_board(self):
        """Расстановка фигур для расширенной игры"""
        super().setup_board()

        # Добавляем шашки
        self.field[5][2] = CheckersFigure("white", (5, 2))
        self.field[5][5] = CheckersFigure("white", (5, 5))
        self.field[2][2] = CheckersFigure("black", (2, 2))
        self.field[2][5] = CheckersFigure("black", (2, 5))

        # Добавляем призраков
        self.field[5][1] = Ghost("white", (5, 1))
        self.field[5][6] = Ghost("white", (5, 6))
        self.field[2][1] = Ghost("black", (2, 1))
        self.field[2][6] = Ghost("black", (2, 6))

        # Добавляем змей
        self.field[5][0] = Snake("white", (5, 0))
        self.field[5][7] = Snake("white", (5, 7))
        self.field[2][0] = Snake("black", (2, 0))
        self.field[2][7] = Snake("black", (2, 7))


class Game:
    """Управляет игрой"""

    def __init__(self, is_chess):
        self.board = Board()
        self.current_player = 'white'
        self.game_over = False
        self.moves = []
        self.is_rock = False
        self.is_chess = is_chess

    def play(self):
        """Запускает игру"""
        while not self.game_over:
            self.board.display_current_board()

            if self.board.is_game_over():
                print(f"Конец игры!! Игрок {self.current_player} проиграл :(")
                self.game_over = True
                continue

            # Проверка рокировки
            if self.is_chess and self.board.if_rock_possible(self.current_player):
                decision = input(f'Игрок {self.current_player}, хотите сделать рокировку? (да/нет):\n')
                if decision.lower() == 'да':
                    self.is_rock = True
                    self.board.rock(self.current_player)
                    self.current_player = "black" if self.current_player == "white" else "white"
                    self.moves = []
                    continue

            if not self.is_rock:
                # Отмена хода
                if self.is_chess:
                    undo_decision = input(f'Игрок {self.current_player}, отменить последний ход? (да/нет):\n')
                    if undo_decision.lower() == 'да':
                        self.board.undo_move()
                        self.current_player = "black" if self.current_player == "white" else "white"
                        continue

                # Ввод хода
                move = input(f'Игрок {self.current_player} делает ход (например: e2 e4):\n').split()

                if len(move) != 2:
                    print("Нужно ввести две клетки")
                    self.moves = []
                    continue

                # Преобразуем координаты
                for step in move:
                    if len(step) != 2:
                        print("Неверный формат координат")
                        self.moves = []
                        break

                    col = step[0].upper()
                    row = step[1]

                    if col not in self.board.letters or row not in self.board.numbers:
                        print("Координаты вне доски")
                        self.moves = []
                        break

                    y = self.board.letters[col] - 1
                    x = int(row) - 1
                    self.moves.append((x, y))

                if len(self.moves) != 2:
                    self.moves = []
                    continue

                # Проверяем и делаем ход
                if self.board.check_move(self.moves[0], self.moves[1]):
                    self.board.make_move(self.moves[0], self.moves[1])

                    # Меняем игрока или продолжаем при множественном взятии
                    if not self.board.field[self.moves[1][0]][self.moves[1][1]].kill:
                        self.current_player = "black" if self.current_player == "white" else "white"
                    else:
                        print(f'Игрок {self.current_player} может бить дальше')
                        self.board.field[self.moves[1][0]][self.moves[1][1]].kill = False

                    self.moves = []
                else:
                    print("Неверный ход, попробуйте снова.")
                    self.moves = []

            self.is_rock = False


class CheckersGame(Game):
    """Игра в шашки"""

    def __init__(self, is_chess):
        super().__init__(is_chess)
        self.board = CheckersBoard()


class ExtendedGame(Game):
    """Расширенная игра"""

    def __init__(self, is_chess):
        super().__init__(is_chess)
        self.board = ExtendedBoard()


# Запуск игры
game_kind = input("Выберите игру: 'шахматы', 'шашки' или 'расширенные шахматы':\n").lower()

if game_kind == 'шахматы':
    game = Game(True)
    game.play()
elif game_kind == 'шашки':
    game = CheckersGame(False)
    game.play()
elif game_kind == 'расширенные шахматы':
    game = ExtendedGame(True)
    game.play()
else:
    print("Неверный ввод. Выберите: 'шахматы', 'шашки' или 'расширенные шахматы'.")
