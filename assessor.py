class Assessor:

    def __init__(self, history):
        self.history = history

    def assess(self):
        lastFive = self.history.get_last(5)
        lastTen = self.history.get_last(10)
        lastTwenty = self.history.get_last(20)
        avLastFive = mean
