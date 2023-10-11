import os

from utils import set_google_application_credentials


class Config:
    # Common configuration settings
    LOG_FOLDER = "logs"
    LOG_FILENAME = "app.log"
    LOG_FILEPATH = os.path.join(LOG_FOLDER, LOG_FILENAME)
    LOG_LEVEL = "INFO"
    LOG_TO_CONSOLE = True
    creds_mapping = {
        "platform1": ("448193001563", "cloud-vision-api-secret-key"),
        "platform2": ("240998976332", "vision-api-secret-key"),
        # Add more platforms as needed
    }
    set_google_application_credentials(creds_mapping)


class ProductionConfig(Config):
    # Production configuration settings
    DEBUG = False
    LOG_LEVEL = "WARNING"


class DevelopmentConfig(Config):
    # Development configuration settings
    DEBUG = True
    LOG_LEVEL = "DEBUG"
