import json
import logging
import os
from google.cloud import secretmanager
from google.api_core import exceptions
from google.auth.exceptions import DefaultCredentialsError

from utils import Path

logger = logging.getLogger(__name__)


class SecretsManager:
    def __init__(self):
        self.client = secretmanager.SecretManagerServiceClient()

    def get_secret(self, project_id, secret_name, version="latest"):
        secret_version_name = (
            f"projects/{project_id}/secrets/{secret_name}/versions/{version}"
        )

        try:
            response = self.client.access_secret_version(
                request={"name": secret_version_name}
            )
            return response.payload.data.decode("UTF-8")
        except exceptions.PermissionDenied:
            return None


def set_google_application_credentials(creds_mapping):
    for platform, (project_id, secret_name) in creds_mapping.items():
        try:
            manager = SecretsManager()
            credentials = manager.get_secret(project_id, secret_name)
            if credentials is not None:
                credentials_json = json.loads(credentials)
                logger.info(f"Sucessfully configured in {platform}")
                break
        except DefaultCredentialsError:
            pass
    else:
        logger.warning("No matching credentials found. Using default Credentials")
        # Fallback to default credentials file if no matching credentials found
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = (
            Path.ROOT_DIR + "/Cloud-vision-api-SA.json"
        )
