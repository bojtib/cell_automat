class Cell:
    def __init__(self, row_index: int, column_index: int, state: bool):
        self.row_index = row_index
        self.column_index = column_index
        self.state = state

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.row_index == other.row_index and self.column_index == other.column_index and self.state == other.state
        else:
            return False

    def __hash__(self):
        return hash((self.row_index, self.column_index, self.state))
