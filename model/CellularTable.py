from model.Cell import Cell


class CellularTable:
    def __init__(self, row_count, column_count):
        self.__table = [[False for x in range(column_count)] for y in range(row_count)]
        self.row_count = row_count
        self.column_count = column_count

    def set_cell(self, row_index, column_index, state: bool):
        self.__table[row_index][column_index] = state

    def is_alive(self, row_index, column_index):
        return self.__table[row_index][column_index]

    def neighbours(self, row_index, column_index):
        neighbours = []
        if self.is_in_the_table(row_index - 1, column_index - 1):
            neighbours.append((row_index - 1, column_index - 1))
        if self.is_in_the_table(row_index - 1, column_index):
            neighbours.append((row_index - 1, column_index))
        if self.is_in_the_table(row_index - 1, column_index + 1):
            neighbours.append((row_index - 1, column_index + 1))
        if self.is_in_the_table(row_index + 1, column_index - 1):
            neighbours.append((row_index + 1, column_index - 1))
        if self.is_in_the_table(row_index + 1, column_index):
            neighbours.append((row_index + 1, column_index))
        if self.is_in_the_table(row_index + 1, column_index + 1):
            neighbours.append((row_index + 1, column_index + 1))
        if self.is_in_the_table(row_index, column_index - 1):
            neighbours.append((row_index, column_index - 1))
        if self.is_in_the_table(row_index, column_index + 1):
            neighbours.append((row_index, column_index + 1))
        return neighbours

    def is_in_the_table(self, row_index, column_index):
        if row_index >= 0 and column_index >= 0 and row_index < self.row_count and column_index < self.column_count:
            return True
        else:
            return False

    # Any live cell with fewer than two live neighbours dies, as if caused by underpopulation.
    # Any live cell with two or three live neighbours lives on to the next generation.
    # Any live cell with more than three live neighbours dies, as if by overpopulation.
    # Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
    def next_state(self, row_index, column_index):
        living_count = 0
        for neighbour in self.neighbours(row_index, column_index):
            living_count += 1 if self.is_alive(neighbour[0], neighbour[1]) else 0

        if self.is_alive(row_index, column_index):
            if living_count < 2 or living_count > 3:
                return False
            else:
                return True
        else:
            if living_count == 3:
                return True
            else:
                return False

    def get_living_cells(self):
        cells = []
        for row_index in range(self.row_count):
            for column_index in range(self.column_count):
                if self.is_alive(row_index, column_index):
                    cells.append(Cell(row_index, column_index, True))
        return cells
