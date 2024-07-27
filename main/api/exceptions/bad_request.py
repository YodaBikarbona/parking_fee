class BadRequestException(Exception):

    def __init__(self, message: str):
        super().__init__('Bad Request')
        self.message = message
        self.status_code = 400
