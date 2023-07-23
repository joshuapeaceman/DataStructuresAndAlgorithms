class Experiment:
    def __init__(self, x, y, capacity):
        self.x = x
        self.y = y
        self.capacity = capacity

        print(self.x, self.y, self.capacity)

    def withinBoundraies(self, x, y):
        if 0 <= x <= self.x and 0 <= y <= self.y:
            return True
        else:
            return False