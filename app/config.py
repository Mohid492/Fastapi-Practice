from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"

settings = Settings()

# reads configuration values from an environment file.
# the file app/config.py is used to read environment variables
# so that they can be accessed throughout the application. The Settings class in
# this file uses Pydantic's BaseSettings to load these variables from an .env file.
# This allows the application to access configuration values such as database
# connection details, secret keys, and other settings