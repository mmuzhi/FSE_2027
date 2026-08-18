import logging
import zipfile
from pathlib import Path
from typing import Optional

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger("org.example.ZipFileProcessor")


def _to_absolute(path: Path) -> Path:
    # Mirrors java.nio.Path.toAbsolutePath(): prefix cwd when relative, no normalization
    return path if path.is_absolute() else Path.cwd() / path


class ZipFileProcessor:

    def __init__(self, zip_file_name: str) -> None:
        self.zip_file_path = Path(zip_file_name)

    def read_zip_file(self) -> Optional[zipfile.ZipFile]:
        if not self.zip_file_path.exists():
            logger.error("Zip file does not exist: %s", _to_absolute(self.zip_file_path))
            return None
        try:
            return zipfile.ZipFile(self.zip_file_path)
        except (OSError, zipfile.BadZipFile):
            logger.error("Failed to read the zip file: %s", _to_absolute(self.zip_file_path), exc_info=True)
            return None

    def extract_all(self, output_dir: str) -> bool:
        output_dir_path = Path(output_dir)
        zip_file = self.read_zip_file()
        if zip_file is None:
            return False
        try:
            if not output_dir_path.exists():
                try:
                    output_dir_path.mkdir(parents=True)
                    logger.info("Created output directory: %s", _to_absolute(output_dir_path))
                except OSError:
                    logger.error("Failed to create output directory: %s", _to_absolute(output_dir_path), exc_info=True)
                    return False

            for entry in zip_file.infolist():
                # Path / str mirrors Path.resolve(other): absolute entry names replace the base
                file_path = output_dir_path / entry.filename
                try:
                    if entry.is_dir():
                        if not file_path.exists():
                            file_path.mkdir(parents=True)
                            logger.info("Created directory: %s", _to_absolute(file_path))
                    else:
                        with zip_file.open(entry) as in_stream, open(file_path, "wb") as out_stream:
                            while True:
                                buffer = in_stream.read(1024)
                                if not buffer:
                                    break
                                out_stream.write(buffer)
                        logger.info("Extracted file: %s", _to_absolute(file_path))
                except (OSError, zipfile.BadZipFile):
                    logger.error("Failed to process entry: %s", entry.filename, exc_info=True)

            return True
        except (OSError, zipfile.BadZipFile):
            logger.error("Failed to extract files from zip: %s", _to_absolute(self.zip_file_path), exc_info=True)
            return False
        finally:
            zip_file.close()

    def extract_file(self, file_name: str, output_dir: str) -> bool:
        output_dir_path = Path(output_dir)
        file_path = output_dir_path / file_name
        zip_file = self.read_zip_file()
        if zip_file is None:
            return False
        try:
            try:
                entry = zip_file.getinfo(file_name)
            except KeyError:
                logger.warning("File not found in zip: %s", file_name)
                return False

            parent = file_path.parent
            if not parent.exists():
                try:
                    parent.mkdir(parents=True)
                    logger.info("Created parent directory: %s", _to_absolute(parent))
                except OSError:
                    logger.error("Failed to create parent directory: %s", _to_absolute(parent), exc_info=True)
                    return False

            with zip_file.open(entry) as in_stream, open(file_path, "wb") as out_stream:
                while True:
                    buffer = in_stream.read(1024)
                    if not buffer:
                        break
                    out_stream.write(buffer)
            logger.info("Extracted file: %s", _to_absolute(file_path))
            return True
        except (OSError, zipfile.BadZipFile):
            logger.error("Failed to extract file: %s", file_name, exc_info=True)
            return False
        finally:
            zip_file.close()