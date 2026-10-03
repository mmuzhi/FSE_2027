import zipfile
from pathlib import Path
import logging

class ZipFileProcessor:
    def __init__(self, zip_filename: str):
        self.zip_file_path = Path(zip_filename)
        self.logger = logging.getLogger(__name__)

    def read_zip_file(self):
        if not self.zip_file_path.exists():
            self.logger.error(f"Zip file does not exist: {self.zip_file_path.absolute()}")
            return None

        try:
            return zipfile.ZipFile(self.zip_file_path, 'r')
        except zipfile.BadZipFile as e:
            self.logger.error(f"Failed to read the zip file: {self.zip_file_path.absolute()}", e)
            return None

    def extract_all(self, output_dir):
        output_dir_path = Path(output_dir)
        zip_file = self.read_zip_file()
        if zip_file is None:
            return False

        try:
            # Create output directory if it doesn't exist
            if not output_dir_path.exists():
                try:
                    output_dir_path.mkdir(parents=True, exist_ok=True)
                    self.logger.info(f"Created output directory: {output_dir_path.absolute()}")
                except OSError as e:
                    self.logger.error(f"Failed to create output directory: {output_dir_path.absolute()}", e)
                    return False

            # Iterate over each entry in the zip file
            for info in zip_file.infolist():
                file_path = output_dir_path / info.filename
                if info.is_dir():
                    # For directories, create the directory
                    try:
                        file_path.mkdir(parents=True, exist_ok=True)
                        self.logger.info(f"Created directory: {file_path.absolute()}")
                    except OSError as e:
                        self.logger.error(f"Failed to create directory: {file_path.absolute()}", e)
                        return False
                else:
                    # For files, extract them
                    try:
                        with zip_file.open(info) as zip_in, open(file_path, 'wb') as out_file:
                            buffer = bytearray(1024)
                            while True:
                                n = zip_in.readinto(buffer)
                                if n == 0:
                                    break
                                out_file.write(buffer[:n])
                            self.logger.info(f"Extracted file: {file_path.absolute()}")
                    except OSError as e:
                        self.logger.error(f"Failed to process entry: {info.filename}", e)
                        return False

            return True

        except Exception as e:
            self.logger.error(f"Failed to extract files from zip: {self.zip_file_path.absolute()}", e)
            return False
        finally:
            if zip_file:
                zip_file.close()

    def extract_file(self, file_name, output_dir):
        output_dir_path = Path(output_dir)
        file_path = output_dir_path / file_name

        zip_file = self.read_zip_file()
        if zip_file is None:
            return False

        try:
            # Check if the file exists in the zip
            if file_name not in zip_file.namelist():
                self.logger.warning(f"File not found in zip: {file_name}")
                return False

            # Create parent directory if needed
            parent_dir = file_path.parent
            if not parent_dir.exists():
                try:
                    parent_dir.mkdir(parents=True, exist_ok=True)
                    self.logger.info(f"Created parent directory: {parent_dir.absolute()}")
                except OSError as e:
                    self.logger.error(f"Failed to create parent directory: {parent_dir.absolute()}", e)
                    return False

            # Extract the file
            with zip_file.open(file_name) as zip_in, open(file_path, 'wb') as out_file:
                buffer = bytearray(1024)
                while True:
                    n = zip_in.readinto(buffer)
                    if n == 0:
                        break
                    out_file.write(buffer[:n])
                self.logger.info(f"Extracted file: {file_path.absolute()}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to extract file: {file_name}", e)
            return False
        finally:
            if zip_file:
                zip_file.close()