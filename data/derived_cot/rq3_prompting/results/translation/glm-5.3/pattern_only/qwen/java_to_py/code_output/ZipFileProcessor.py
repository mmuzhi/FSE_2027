import logging
import zipfile
from pathlib import Path

logger = logging.getLogger("org.example.ZipFileProcessor")


class ZipFileProcessor:

    def __init__(self, zip_file_name):
        self._zip_file_path = Path(zip_file_name)

    def _read_zip_file(self):
        if not self._zip_file_path.exists():
            logger.log(logging.ERROR,
                       "Zip file does not exist: " + str(self._zip_file_path.absolute()))
            return None
        try:
            return zipfile.ZipFile(self._zip_file_path)
        except (OSError, zipfile.BadZipFile):
            logger.log(logging.ERROR,
                       "Failed to read the zip file: " + str(self._zip_file_path.absolute()),
                       exc_info=True)
            return None

    def extract_all(self, output_dir):
        output_dir_path = Path(output_dir)
        zip_file = self._read_zip_file()
        if zip_file is None:
            return False
        try:
            try:
                if not output_dir_path.exists():
                    try:
                        output_dir_path.mkdir(parents=True)
                        logger.info("Created output directory: " + str(output_dir_path.absolute()))
                    except (OSError, zipfile.BadZipFile):
                        logger.log(logging.ERROR,
                                   "Failed to create output directory: " + str(output_dir_path.absolute()),
                                   exc_info=True)
                        return False

                for entry in zip_file.infolist():
                    file_path = output_dir_path / entry.filename
                    try:
                        if entry.is_dir():
                            if not file_path.exists():
                                file_path.mkdir(parents=True)
                                logger.info("Created directory: " + str(file_path.absolute()))
                        else:
                            with zip_file.open(entry) as in_stream, \
                                 open(file_path, "wb") as out_stream:
                                chunk = in_stream.read(1024)
                                while chunk:
                                    out_stream.write(chunk)
                                    chunk = in_stream.read(1024)
                            logger.info("Extracted file: " + str(file_path.absolute()))
                    except (OSError, zipfile.BadZipFile):
                        logger.log(logging.ERROR,
                                   "Failed to process entry: " + entry.filename,
                                   exc_info=True)

                return True
            finally:
                zip_file.close()
        except (OSError, zipfile.BadZipFile):
            logger.log(logging.ERROR,
                       "Failed to extract files from zip: " + str(self._zip_file_path.absolute()),
                       exc_info=True)
            return False

    def extract_file(self, file_name, output_dir):
        output_dir_path = Path(output_dir)
        file_path = output_dir_path / file_name
        zip_file = self._read_zip_file()
        if zip_file is None:
            return False
        try:
            try:
                try:
                    entry = zip_file.getinfo(file_name)
                except KeyError:
                    entry = None
                if entry is None:
                    logger.warning("File not found in zip: " + file_name)
                    return False

                parent = file_path.parent
                if not parent.exists():
                    try:
                        parent.mkdir(parents=True)
                        logger.info("Created parent directory: " + str(parent.absolute()))
                    except (OSError, zipfile.BadZipFile):
                        logger.log(logging.ERROR,
                                   "Failed to create parent directory: " + str(parent.absolute()),
                                   exc_info=True)
                        return False

                with zip_file.open(entry) as in_stream, \
                     open(file_path, "wb") as out_stream:
                    chunk = in_stream.read(1024)
                    while chunk:
                        out_stream.write(chunk)
                        chunk = in_stream.read(1024)
                logger.info("Extracted file: " + str(file_path.absolute()))

                return True
            finally:
                zip_file.close()
        except (OSError, zipfile.BadZipFile):
            logger.log(logging.ERROR,
                       "Failed to extract file: " + file_name,
                       exc_info=True)
            return False