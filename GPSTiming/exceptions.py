class NoGPSTriggers(ValueError):
    def __init__(self, message="No GPS Triggers in table."):
        super().__init__(message)
