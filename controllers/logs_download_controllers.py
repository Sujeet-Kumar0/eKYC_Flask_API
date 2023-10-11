import shutil
import logging

logger = logging.getLogger(__name__)

class LogsDownloadController:
    def __init__(self, folder_path, temp_zip_path):
        self.folder = folder_path
        self.zip_file = temp_zip_path

    def download_folder_path(self):
        logger.info("Zipping.....")
        shutil.make_archive(self.zip_file[:-4], "zip", self.folder)
        logger.info("Zipping Completed.....")
        return self.zip_file
