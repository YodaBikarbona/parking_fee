class NotFoundException(Exception):

    def __init__(self, message: str):
        super().__init__('Not Found')
        self.message = message
        self.status_code = 404
