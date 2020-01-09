from .need import Need
from .exceptions import NeedyStatesHandlerException, NeedyStatesNoMatch


class NeedProcessor(object):

    def __init__(self):
        """
        A NeedProcessor is a class that is used to marshall and execute actions based on supplied needs.
        """
        self.unsated_needs = []
        self.sated_needs = []
        self.handlers = []

    def add_need(self, need: Need):
        """
        Add a need to the processor
        :param need:
            A single Need instance
        """
        self.unsated_needs.append(need)

    def add_needs(self, needs: list):
        """
        Add a list of needs to the processor
        :param needs:
            A list of Need Instances
        """
        for item in needs:
            self.unsated_needs.append(item)

    def mark_sated(self, need):
        """
        Mark a need as complete
        :param need:
            The need Instance to be marked complete (sated)
        """
        self.unsated_needs.pop(self.unsated_needs.index(need))
        self.sated_needs.append(need)

    def add_handler(self, handler):
        """
        Adds a handler action to the processor, must be decorated with the "need_handler" decorator
        :param handler:
            A decorated function to be used as a need processor
        """
        self.handlers.append(handler)

    def handle_needs(self):
        """
        Iterates through needs and handlers to
        :return:
        """
        sated_needs = []
        for need in self.unsated_needs:
            for handler in self.handlers:
                try:
                    handler(need)
                    sated_needs.append(need)
                except NeedyStatesNoMatch:
                    pass
                except Exception as e:
                    raise NeedyStatesHandlerException(f"An error occurred while handling need {need.get_short_string()}:"
                                                      f"{e}")
        for need in sated_needs:
            self.mark_sated(need)
