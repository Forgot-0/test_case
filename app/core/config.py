from pydantic import Field
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
load_dotenv()


class Email(BaseSettings):
    username: str = Field(alias="EMAIL_USERNAME")
    password: str = Field(alias="EMAIL_PASSWORD")
    from_email: str = Field(alias="EMAIL_FROM")
    port: int = Field(default=587, alias="EMAIL_PORT")
    server: str = Field(alias="EMAIL_SERVER")
    starttls: bool = Field(default=True, alias="EMAIL_STARTTLS")
    ssl_tls: bool = Field(default=False, alias="EMAIL_SSL_TLS")
    use_credentials: bool = Field(default=True, alias="USE_CREDENTIALS")
    validate_certs: bool = Field(default=True, alias="VALIDATE_CERTS")


class API(BaseSettings):
    port: int = Field(alias='API_PORT')
    secret: str = Field(alias='SECRET')
    algorithm: str = Field(alias='ALGORITHM')
    watermark_path: str = Field(alias='WATERMAKR_PATH')


class DataBase(BaseSettings):
    db: str = Field(alias='POSTGRES_DB')
    username: str = Field(alias='POSTGRES_USER')
    password: str = Field(alias='POSTGRES_PASSWORD')
    port: str = Field(alias='POSTGRES_PORT')
    host: str = Field(alias='POSTGRES_HOST')

    @property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.username}:{self.password}@{self.host}:{self.port}/{self.db}"

    @property
    def test_postgres_db(self) -> str:
        return f"test_{self.db}"

    @property
    def test_postgres_url(self) -> str:
        return f"postgresql+asyncpg://{self.username}:{self.password}@{self.host}:{self.port}/{self.test_postgres_db}"


class Redis(BaseSettings):
    host: str = Field(alias="REDIS_HOST")
    port: str = Field(alias="REDIS_PORT")


class Config:
    api = API()
    db = DataBase()
    email = Email()
    redis = Redis()

settings = Config()
