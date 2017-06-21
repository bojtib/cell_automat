from model.CellularTable import CellularTable
from model.Cell import Cell
import time


class Simulation:
    def __init__(self, cellular_table: CellularTable):
        self.__cellular_table = cellular_table
        self.__listeners = []
        self.running = False

    def start(self, default_state: [Cell]):
        change_set = set(default_state)
        while self.running:
            if len(change_set) == 0:
                self.running = False
                break
            print("Changed status: ", len(change_set))
            self.set_table(change_set)
            self.notify_all(change_set)
            time.sleep(1)
            new_change_set = set()
            for change in change_set:
                new_change_set |= set(self.check_neighbours_and_self(change.row_index, change.column_index))
            change_set = new_change_set

    def stop(self):
        self.running = False

    def set_table(self, change_set: [Cell]):
        for cell_state in change_set:
            self.__cellular_table.set_cell(cell_state.row_index, cell_state.column_index, cell_state.state)

    def add_listener(self, listener):
        self.__listeners.append(listener)

    def notify_all(self, change_set):
        for listener in self.__listeners:
            listener(change_set)

    def check_neighbours_and_self(self, row_index, column_index):
        change_set = []
        next_state = self.__cellular_table.next_state(row_index, column_index)
        if self.__cellular_table.is_alive(row_index, column_index) != next_state:
            change_set.append(Cell(row_index, column_index, next_state))
        for neighbour in self.__cellular_table.neighbours(row_index, column_index):
            next_state = self.__cellular_table.next_state(neighbour[0], neighbour[1])
            if self.__cellular_table.is_alive(neighbour[0], neighbour[1]) != next_state:
                change_set.append(Cell(neighbour[0], neighbour[1], next_state))

        return change_set
