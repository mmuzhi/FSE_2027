import logging
import os
import zipfile
from pathlib import Path

logger = logging.getLogger("org.example.ZipFileProcessor")


def _java_parent(output_dir, file_name):
    if file_name == "":
        combined = output_dir
    else:
        combined = os.path.join(output_dir, file_name)

    stripped = combined.rstrip("/\\")
    if stripped == "":
        stripped = combined

    parent = os.path.dirname(stripped)
    if parent == "" or parent == stripped:
        return None
    return parent


class ZipFileProcessor:
    def __init__(self, zipFileName):
        self.zip_file_path = Path(zipFileName)

    def readZipFile(self):
        if not self.zip_file_path.exists():
            logger.critical("Zip file does not exist: %s", self.zip_file_path.absolute())
            return None
        try:
            return zipfile.ZipFile(self.zip_file_path, 'r')
        except (OSError, zipfile.BadZipFile) as e:
            logger.critical("Failed to read the zip file: %s", self.zip_file_path.absolute(), exc_info=True)
            return None

    def extractAll(self, outputDir):
        output_dir_path = Path(outputDir)
        zip_file = self.readZipFile()
        if zip_file is None:
            return False

        try:
            with zip_file:
                if not output_dir_path.exists():
                    try:
                        output_dir_path.mkdir(parents=True, exist_ok=True)
                        logger.info("Created output directory: %s", output_dir_path.absolute())
                    except OSError as e:
                        logger.critical("Failed to create output directory: %s", output_dir_path.absolute(), exc_info=True)
                        return False

                for entry in zip_file.infolist():
                    file_path = output_dir_path / entry.filename
                    try:
                        if entry.is_dir():
                            if not file_path.exists():
                                file_path.mkdir(parents=True, exist_ok=True)
                                logger.info("Created directory: %s", file_path.absolute())
                        else:
                            with zip_file.open(entry) as in_file, open(file_path, 'wb') as out_file:
                                while True:
                                    data = in_file.read(1024)
                                    if not data:
                                        break
                                    out_file.write(data)
                            logger.info("Extracted file: %s", file_path.absolute())
                    except (OSError, zipfile.BadZipFile, RuntimeError) as e:
                        logger.critical("Failed to process entry: %s", entry.filename, exc_info=True)

            return True
        except (OSError, zipfile.BadZipFile, RuntimeError) as e:
            logger.critical("Failed to extract files from zip: %s", self.zip_file_path.absolute(), exc_info=True)
            return False

    def extractFile(self, fileName, outputDir):
        output_dir_path = Path(outputDir)
        file_path = output_dir_path / fileName
        zip_file = self.readZipFile()
        if zip_file is None:
            return False

        try:
            with zip_file:
                try:
                    entry = zip_file.getinfo(fileName)
                except KeyError:
                    logger.warning("File not found in zip: %s", fileName)
                    return False

                parent_str = _java_parent(outputDir, fileName)
                parent = Path(parent_str) if parent_str else None

                if not parent.exists():
                    try:
                        parent.mkdir(parents=True, exist_ok=True)
                        logger.info("Created parent directory: %s", parent.absolute())
                    except OSError as e:
                        logger.critical("Failed to create parent directory: %s", parent.absolute(), exc_info=True)
                        return False

                if entry.is_dir():
                    with open(file_path, 'wb') as out_file:
                        pass
                else:
                    with zip_file.open(entry) as in_file, open(file_path, 'wb') as out_file:
                        while True:
                            data = in_file.read(1024)
                            if not data:
                                break
                            out_file.write(data)

                logger.info("Extracted file: %s", file_path.absolute())
                return True
        except (OSError, zipfile.BadZipFile, RuntimeError) as e:
            logger.critical("Failed to extract file: %s", fileName, exc_info=True)
            return False