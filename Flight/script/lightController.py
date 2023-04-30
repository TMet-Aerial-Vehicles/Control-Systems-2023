

class LightController:

    def __init__(self):
        # Bool to represent Light status, False is Off, True is On
        self.status = False

    def turn_on(self):
        self.status = True
        # TODO:

    def turn_off(self):
        self.status = False
        # TODO:

    def get_status(self):
        return self.status
