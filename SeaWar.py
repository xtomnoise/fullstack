import random
import itertools


class NotTwoErr(Exception):
    ...


class OutofRangeErr(Exception):
    ...


class RepeatErr(Exception):
    ...


class Ship:
    def init_cells(self):
        _damage = None  # ['0', 'X', '■'] список повреждений ячеек корабля
        _status = None  # 'Dead' / 'Alive'
        _cells = None  # [(1,0),(1,1)]
        _cords = None  # (x, y)
        _horis = None  # 1 / 0
        _size = None  # 1, 2, 3
        self._cells = []
        self._damage = []
        
        if self.horis:
            for i in range(self._size):
                self._cells.append((self._cords[0], self._cords[1] + i))
        else:
            for i in range(self._size):
                self._cells.append((self._cords[0] + i, self._cords[1]))
            self._damage.append('0')

    def strike(self, value):
        self._damage[self._cells.index(value)] = 'X'

    @property
    def status(self):
        if not self._damage.count('0'):
            for i in range(self._size):
                self._damage[i] = '■'
            self._status = 'Dead'
            return self._status
        else:
            self._status = 'Alive'
            return self._status

    @property
    def cells(self):
        return self._cells

    @property
    def cords(self):
        return self._cords

    @cords.setter
    def cords(self, value):
        self._cords = value

    @property
    def horis(self):
        return self._horis

    @horis.setter
    def horis(self, value):
        self._horis = value

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self._size = value

    @property
    def damage(self):
        return self._damage


class Field:

    def __init__(self, player, size_list, size_field):  # рисуем корабли, сохраняя области, куда нельзя
        self._ships = []
        self._field = set()
        self._reserved_cells = set()
        self._shoot_history = set()
        self._shoot_cord = None
        self.player = player
        self._size_field = size_field
        self.ships_amount = len(size_list)

        for i, j in itertools.product(range(1, self._size_field + 1),
                                      range(1, self._size_field + 1)):
            self._field.add((i, j))
            # регаем игровое поле

        for i, j in itertools.product(range(1, self._size_field + 1),
                                      range(self._size_field + 1, self._size_field + 3)):
            self._reserved_cells.add((i, j))
            self._reserved_cells.add((j, i))
            # зарезервируем запрещ поля - на них нельзя

        for i in range(self.ships_amount):  # генерим корабли
            while True:
                self._ships.append(Ship())
                self._ships[i].cords = (random.randint(1, self._size_field),
                                        random.randint(1, self._size_field))
                self._ships[i].horis = random.randint(0, 1)
                self._ships[i].size = size_list[i]
                self._ships[i].init_cells()

                set_cells = set(self._ships[i].cells)  # временная переменная для проверки пересечения с резерв. обл.
                if set_cells.intersection(self._reserved_cells):  # если ячейки пересекаются с резерв. областью
                    self._ships.pop()  # удаляем корабль и пробуем нарисовать его снова
                    continue
                else:
                    break  # всё ок, рисуем следующий

            self._reserved_cells.update(self.rect_around_ship(i))
            # добавляем в резерерв прямоугольную область вокруг корабля

    def rect_around_ship(self, k):  # функция вычисления координат ячеек вокруг корабля по его индексу
        left_x_res = self._ships[k].cells[0][0] - 1
        right_x_res = self._ships[k].cells[self._ships[k].size - 1][0] + 1
        top_y_res = self._ships[k].cells[0][1] - 1
        bott_y_res = self._ships[k].cells[self._ships[k].size - 1][1] + 1

        lst = set()
        for i, j in itertools.product(range(left_x_res, right_x_res + 1),
                                      range(top_y_res, bott_y_res + 1)):
            lst.add((i, j))
            # добавляем в список ячейки корабля и вокруг него
        return lst

    # Отрисовка доски
    def draw_field(self):
        symbol = None  # символ '0' если свой корабль, '-' если ии

        if not self.player:
            print('Ваше поле:')
        else:
            print('Поле ИИ:')

        top_str = []  # верхняя шкала
        for i in range(1, self._size_field + 1):
            top_str.append(i)
        print(' ', *top_str)

        for i in range(1, self._size_field + 1):  # проходимся по всем строкам
            line = []

            for j in range(1, self._size_field + 1):  # проходимся по всем столбцам
                for k in range(len(self._ships)):  # проходимся по всем кораблям
                    if (i, j) in self._ships[k].cells:  # есть ли такая ячейка в корабле
                        symbol = '-' if self.player else '0'  # проверяем чей корабль рисуем
                        if (self._ships[k].damage[self._ships[k].cells.index((i, j))] == '0'):
                            # если рисуем нетронутую обл корабля
                            line.append(symbol)  # '0' для игрока, '-' для ии
                        else:
                            line.append(self._ships[k].damage[self._ships[k].cells.index((i, j))])
                            # рисуем содержимое damage с индексом, равным индексу ячейки корабля с координатами (i, j)
                        break
                else:  # когда прошлись по координатам ячеек кораблей, идём по координатам поля
                    if (i, j) in self._shoot_history:  # нет в коорд кораблей, но есть в коорд истории выстрелов
                        line.append('T')
                    else:
                        line.append('-')

            print(str(i), *line)

    @property
    def free_field_cells(self):
        return list(self._field.difference(self._shoot_history))

    def get_move(self):
        print('\n')
        shoot_cord = list(input('      Ваш ход:').split())
        try:
            shoot_cord = tuple(map(int, shoot_cord))

            if len(shoot_cord) != 2:
                raise NotTwoErr

            if (self._size_field < shoot_cord[0]
                    or self._size_field < shoot_cord[1]
                    or shoot_cord[0] < 1
                    or shoot_cord[1] < 1):
                raise OutofRangeErr

            if shoot_cord in self._shoot_history:
                raise RepeatErr

        except ValueError:
            print('Введите числа')
            return 'Error'
        except NotTwoErr:
            print('Введите 2 числа')
            return 'Error'
        except OutofRangeErr:
            print(f'Введите числа от 1 до {self._size_field}')
            return 'Error'
        except RepeatErr:
            print('Клетка уже поражена')
            return 'Error'

        else:
            self._shoot_cord = shoot_cord
            return 'Success'

    def rand_move(self):
        self._shoot_cord = random.choice(self.free_field_cells)
        print('\n')
        print('      Ход ИИ:', *self._shoot_cord)

    def shoot(self):
        for k in range(self.ships_amount):
            if self._shoot_cord in self._ships[k].cells:
                self._ships[k].strike(self._shoot_cord)
                self._shoot_history.add(self._shoot_cord)
                if self._ships[k].status == 'Dead':
                    print('***** УБИЛ!')  # СДЕЛАТЬ ФУНКЦИЕЙ
                    self._shoot_history.update(self.rect_around_ship(k))
                    # добавляем в историю выстрелов прямоугольную область вокруг корабля
                else:
                    print('***** ПОПАЛ')
                return 'Hit'
        else:
            self._shoot_history.add(self._shoot_cord)
            print('***** МИМО')
            return 'Miss'

    # Проверка выигрыша
    def dead_field_check(self):
        deadships = 0
        for k in range(self.ships_amount):
            if self._ships[k].status == 'Dead':
                deadships += 1
        if deadships == self.ships_amount:  # если кол-во кораблей = кол-во Dead кораблей, конец игры
            return True
        else:
            return False


size_list = [3, 2, 2, 1, 1, 1, 1]
size_field = 6
plid = 0  # первым ходит игрок
step = 0

fields = [Field(0, size_list, size_field),
          Field(1, size_list, size_field)]
try:
    while True:
        fields[0].draw_field()  # поле игрока
        fields[1].draw_field()  # поле ии
        plid = step % 2

        if not plid:  # ход игрока

            while fields[1].get_move() != 'Success':
                ...

            while fields[1].shoot() != 'Miss':  # поле обрабатывает выстрел
                if fields[1].dead_field_check():  # поле проверяет, есть ли живые корабли
                    raise StopIteration
                fields[0].draw_field()
                fields[1].draw_field()
                while fields[1].get_move() != 'Success':
                    ...

        else:  # ход ии
            fields[0].rand_move()
            while fields[0].shoot() != 'Miss':  # поле обрабатывает выстрел
                if fields[0].dead_field_check():  # поле проверяет, есть ли живые корабли
                    raise StopIteration
                fields[0].draw_field()
                fields[1].draw_field()
                fields[0].rand_move()

        step += 1

except StopIteration:
    if plid == 0:
        fields[0].draw_field()
        fields[1].draw_field()
        print('***** Вы победили! *****')

    else:
        fields[0].draw_field()
        fields[1].draw_field()
        print('***** Победил ИИ! *****')
    input()
