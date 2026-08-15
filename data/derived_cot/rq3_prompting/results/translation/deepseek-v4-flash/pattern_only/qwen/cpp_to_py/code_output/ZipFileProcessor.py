import os
import sys
import zipfile


class ZipFileInfo:
    def __init__(self, filename="", mode=""):
        self.filename = filename
        self.mode = mode


class ZipFileProcessor:
    def __init__(self, zip_file_path):
        self.zip_file_path_ = zip_file_path

    def _open_zip_file(self, mode):
        try:
            return zipfile.ZipFile(self.zip_file_path_, mode)
        except Exception:
            print("Failed to open zip file: " + self.zip_file_path_, file=sys.stderr)
            return None

    def _create_directory_if_not_exists(self, dir_path):
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        return True

    def _extract_file_from_zip(self, archive, file_name, output_file_path):
        # libzip's zip_fopen fails for directory entries
        if file_name.endswith("/"):
            print("Failed to open file in zip: " + file_name, file=sys.stderr)
            return False

        try:
            zf = archive.open(file_name, "r")
        except Exception:
            print("Failed to open file in zip: " + file_name, file=sys.stderr)
            return False

        try:
            try:
                out_file = open(output_file_path, "wb")
            except OSError:
                print("Failed to open output file: " + output_file_path, file=sys.stderr)
                return False

            try:
                while True:
                    try:
                        buf = zf.read(4096)
                    except Exception:
                        # zip_fread returning <= 0 is not treated as an error by the original code
                        break
                    if not buf:
                        break
                    try:
                        out_file.write(buf)
                    except OSError:
                        print("Failed to write to file: " + output_file_path, file=sys.stderr)
                        return False
            finally:
                out_file.close()
        finally:
            zf.close()

        return True

    def read_zip_file(self):
        archive = self._open_zip_file("r")
        info = ZipFileInfo()
        if archive is not None:
            info.filename = self.zip_file_path_
            info.mode = "r"
            archive.close()
        return info

    def extract_all(self, output_directory):
        if not output_directory:
            return False

        if not self._create_directory_if_not_exists(output_directory):
            return False

        archive = self._open_zip_file("r")
        if archive is None:
            return False

        success = True
        try:
            for info in archive.infolist():
                name = info.filename
                output_file_path = output_directory + "/" + name
                if not self._extract_file_from_zip(archive, name, output_file_path):
                    success = False
        finally:
            archive.close()

        return success

    def extract_file(self, file_name, output_directory):
        if not output_directory:
            return False

        if not self._create_directory_if_not_exists(output_directory):
            print("Failed to create output directory: " + output_directory, file=sys.stderr)
            return False

        archive = self._open_zip_file("r")
        if archive is None:
            return False

        try:
            if file_name not in archive.namelist():
                print("File not found in zip: " + file_name, file=sys.stderr)
                return False

            output_file_path = output_directory + "/" + file_name
            return self._extract_file_from_zip(archive, file_name, output_file_path)
        finally:
            archive.close()

    def create_zip_file(self, files, output_zip_file):
        try:
            archive = zipfile.ZipFile(output_zip_file, "w")
        except Exception:
            print("Error opening zip file: " + output_zip_file, file=sys.stderr)
            return False

        try:
            for file_path in files:
                try:
                    archive.write(file_path, arcname=file_path)
                except OSError:
                    # In libzip, missing/unreadable files are usually detected at zip_close
                    print("Error closing zip file: " + output_zip_file, file=sys.stderr)
                    try:
                        archive.close()
                    except Exception:
                        pass
                    return False
                except Exception:
                    print("Error adding file to zip: " + file_path, file=sys.stderr)
                    try:
                        archive.close()
                    except Exception:
                        pass
                    return False

            try:
                archive.close()
            except Exception:
                print("Error closing zip file: " + output_zip_file, file=sys.stderr)
                return False

            return True
        except Exception:
            try:
                archive.close()
            except Exception:
                pass
            return False