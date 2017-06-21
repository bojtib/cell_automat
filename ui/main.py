from _thread import start_new_thread
from tkinter import *

from model.Cell import Cell
from model.CellularTable import CellularTable
from simulation.Simulation import Simulation


class App:
    def __init__(self, master, cellular_table: CellularTable):
        self.separator = ";"
        self.simulation = Simulation(cellular_table)
        self.simulation.add_listener(self.listener)

        frame = Frame(master)
        frame.pack()

        self.start_btn = Button(
            frame, text="Start", command=self.start
        )
        self.start_btn.pack(side=LEFT)

        self.stop_btn = Button(
            frame, text="Stop", command=self.stop
        )
        self.stop_btn.pack(side=RIGHT)

        self.button = Button(
            frame, text="QUIT", command=frame.quit
        )
        self.button.pack(side=BOTTOM)

        self.offset = 10
        self.canvas_width = 700
        self.canvas_height = 700

        self.cellular_table = cellular_table

        self.cell_width = (self.canvas_width - self.offset * 2) / self.cellular_table.column_count
        self.cell_height = (self.canvas_height - self.offset * 2) / self.cellular_table.row_count

        self.canvas = Canvas(frame, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack(side=TOP)
        self.draw_cells()

    def draw_cells(self):
        for row_index in range(self.cellular_table.row_count):
            for col_index in range(self.cellular_table.column_count):
                self.draw_cell(row_index, col_index)

    def draw_cell(self, row_index, col_index):
        color = "white"
        tag = str(row_index) + self.separator + str(col_index)
        item = self.canvas.create_rectangle(self.cell_width * col_index + self.offset,
                                            self.cell_height * row_index + self.offset,
                                            self.cell_width * (col_index + 1) + self.offset,
                                            self.cell_height * (row_index + 1) + self.offset, fill=color,
                                            tags=tag)
        self.canvas.tag_bind(item, '<Button-1>', self.on_rectangle_click)

    def on_rectangle_click(self, event):
        if not self.simulation.running:
            item = event.widget.find_closest(event.x, event.y)
            tags = event.widget.gettags(item)[0].split(self.separator)
            print("Clicked on: ", tags)
            row_index = int(tags[0])
            column_index = int(tags[1])
            self.cellular_table.set_cell(row_index, column_index,
                                         not self.cellular_table.is_alive(row_index, column_index))
            self.change_cell(row_index, column_index, self.cellular_table.is_alive(row_index, column_index))

    def change_cell(self, row_index, column_index, state):
        color = "white"
        if state:
            color = "red"

        item = self.canvas.find_withtag(str(row_index) + self.separator + str(column_index))
        self.canvas.itemconfig(item, fill=color)

    def listener(self, change_set: [Cell]):
        for cell in change_set:
            self.change_cell(cell.row_index, cell.column_index, cell.state)

    def start(self):
        self.simulation.running = True
        cells = self.cellular_table.get_living_cells()
        start_new_thread(self.simulation.start, (cells,))

    def stop(self):
        self.simulation.running = False



if __name__ == '__main__':
    root = Tk()
    cellular_table = CellularTable(50, 50)
    app = App(root, cellular_table)
    root.mainloop()
