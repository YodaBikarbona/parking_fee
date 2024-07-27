class DecodeTokenException(Exception):

    def __init__(self, message: str):
        super().__init__('DecodeTokenException')
        self.message = message
        self.status_code = 400
