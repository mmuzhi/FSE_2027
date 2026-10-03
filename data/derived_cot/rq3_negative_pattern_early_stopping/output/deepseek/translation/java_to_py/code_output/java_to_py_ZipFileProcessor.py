import logging
import zipfile
from pathlib import Path

logger = logging.getLogger(__name__)


class ZipFileProcessor:
    def __init__(self, zip_file_name: str):
        self.zip_file_path = Path(zip_file_name)

    def _read_zip_file(self):
        if not self.zip_file_path.exists():
            logger.log(logging.ERROR, f"Zip file does not exist: {self.zip_file_path.resolve()}")
            return None
        try:
            return zipfile.ZipFile(str(self.zip_file_path), 'r')
        except (zipfile.BadZipFile, FileNotFoundError, IOError) as e:
            logger.log(logging.ERROR,
                       f"Failed to read the zip file: {self.zip_file_path.resolve()}", exc_info=e)
            return None

    def extract_all(self, output_dir: str) -> bool:
        output_dir_path = Path(output_dir)
        zip_file = self._read_zip_file()
        if zip_file is None:
            return False

        try:
            if not output_dir_path.exists():
                try:
                    output_dir_path.mkdir(parents=True)
                    logger.info(f"Created output directory: {output_dir_path.resolve()}")
                except (FileNotFoundError, IOError) as e:
                    logger.log(logging.ERROR,
                               f"Failed to create output directory: {output_dir_path.resolve()}", exc_info=e)
                    return False

            for entry in zip_file.infolist():
                file_path = output_dir_path / entry.filename
                try:
                    if entry.is_dir():
                        if not file_path.exists():
                            file_path.mkdir(parents=True)
                            logger.info(f"Created directory: {file_path.resolve()}")
                    else:
                        with zip_file.open(entry, 'r') as in_stream:
                            in_stream._orig_buffer_size = 1024  # not needed, but kept for buffer size consistency
                            with open(str(file_path), 'wb') as out_stream:
                                buffer = bytearray(1024)
                                while True:
                                    length = in_stream.readinto(buffer)
                                    if length == 0:
                                        break
                                    out_stream.write(buffer[:length])
                                logger.info(f"Extracted file: {file_path.resolve()}")
                except (IOError, FileNotFoundError) as e:
                    logger.log(logging.ERROR, f"Failed to process entry: {entry.filename}", exc_info=e)
            return True
        except (IOError, zipfile.BadZipFile) as e:
            logger.log(logging.ERROR,
                       f"Failed to extract files from zip: {self.zip_file_path.resolve()}", exc_info=e)
            return False
        finally:
            zip_file.close()

    def extract_file(self, file_name: str, output_dir: str) -> bool:
        output_dir_path = Path(output_dir)
        file_path = output_dir_path / file_name
        zip_file = self._read_zip_file()
        if zip_file is None:
            return False

        try:
            try:
                entry = zip_file.getinfo(file_name)
            except KeyError:
                logger.warning(f"File not found in zip: {file_name}")
                return False

            parent_dir = file_path.parent
            if not parent_dir.exists():
                try:
                    parent_dir.mkdir(parents=True)
                    logger.info(f"Created parent directory: {parent_dir.resolve()}")
                except (IOError, FileNotFoundError) as e:
                    logger.log(logging.ERROR,
                               f"Failed to create parent directory: {parent_dir.resolve()}", exc_info=e)
                    return False

            with zip_file.open(entry, 'r') as in_stream:
                with open(str(file_path), 'wb') as out_stream:
                    while True:
                        chunk = in_stream.read(1024)
                        if not chunk:
                            break
                        out_stream.write(chunk)
                    logger.info(f"Extracted file: {file_path.resolve()}")
            return True
        except (IOError, zipfile.BadZipFile) as e:
            logger.log(logging.ERROR, f"Failed to extract file: {file_name}", exc_info=e)
            return False
        finally:
            zip_file.close()