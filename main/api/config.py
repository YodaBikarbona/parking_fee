from pydantic.v1 import BaseSettings, validator

from main.api.utils.util import generate_random_string


class Settings(BaseSettings):

    debug: bool = False

    route: str = '/api/v1'
    description: str = 'RestAPI Service'

    server_type: str

    # Database parameters
    driver_name: str = 'postgresql://'
    database_type: str = 'postgresql'
    postgres_username: str
    postgres_password: str
    postgres_host: str
    postgres_port: str
    postgres_database: str

    # JWT secret
    jwt_access_secret_key: str = generate_random_string(size=255)
    jwt_refresh_secret_key: str = generate_random_string(size=255)

    @validator('server_type')
    def validate_server_type(cls, value):
        if value not in {'dev', 'prod', 'local'}:
            raise ValueError('server_type must be one of: dev, prod, local')
        return value


settings = Settings()
