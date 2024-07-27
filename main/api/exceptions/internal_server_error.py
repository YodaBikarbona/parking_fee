class InternalServerErrorException(Exception):

    def __init__(self):
        super().__init__('Internal Server Error')
        self.message = 'Something went wrong'
        self.status_code = 500
