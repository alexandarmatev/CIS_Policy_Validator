class MissingAttributeError(Exception):
    def __init__(self, attribute):
        self.attribute = attribute
        self.message = f"'{self.attribute}' attribute is empty or does not exist in the configuration file."
        super().__init__(self.message)

