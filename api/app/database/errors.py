class ObjectAlreadyExistsException(Exception):
    def __init__(self, obj):
        self.obj = obj