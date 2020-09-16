class Assessor:

    def __init__(self, history):
        self.history = history

    def last_x_av(self, x):
        sliceLen = min(x, len(self.history.data))
        if sliceLen == 0:
            return 1.
        else:
            sliceData = [row[2] for row in self.history.data[-sliceLen:]]
            average = sum(sliceData) / sliceLen
        return average

    def assess(self):
        allAv = \
            0.5 * self.last_x_av(5) \
            + 0.25 * self.last_x_av(10) \
            + 0.125 * self.last_x_av(20) \
            + 0.125 * self.last_x_av(50)
        return allAv
