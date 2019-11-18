class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"[{self.x}, {self.y}]"

    def __sub__(self, other):
        if type(other).__name__ != "Position":
            return None
        return Position(abs(self.x - other.x), abs(self.y - other.y))

    def __getitem__(self, index):
        if index == 'x':
            return self.x
        elif index == 'y':
            return self.y
        else:
            raise KeyError("The Key can be only x and y.")