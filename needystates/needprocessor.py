from .need import Need


class NeedProcessor(object):

    def __init__(self):
        self.unsated_needs = []
        self.sated_needs = []
        self.handlers = []

    def add_need(self, need: Need):
        self.unsated_needs.append(need)

    def add_needs(self, needs: list):
        for item in needs:
            self.unsated_needs.append(item)

    def mark_sated(self, need):
        self.unsated_needs.pop(self.unsated_needs.index(need))
        self.sated_needs.append(need)
