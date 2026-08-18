import os
import sys
import zipfile


class ZipFileInfo:
    def __init__(self, filename="", mode=""):
        self.filename = filename
        self.mode = mode


class ZipFileProcessor:
    def __init__(self, zip_file_path):
        self._zip_file_path = zip_file_path

    def read_zip_file(self):
        archive = self._open_zip_file("r")
        info = ZipFileInfo()
        if archive is not None:
            info.filename = self._zip_file_path
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
        names = archive.namelist()
        for i in range(len(names)):
            output_file_path = output_directory + "/" + names[i]
            if not self._extract_file_from_zip(archive, i, output_file_path):
                success = False

        archive.close()
        return success

    def extract_file(self, file_name, output_directory):
        if not output_directory:
            return False

        if not self._create_directory_if_not_exists(output_directory):
            print(f"Failed to create output directory: {output_directory}", file=sys.stderr)
            return False

        archive = self._open_zip_file("r")
        if archive is None:
            return False

        names = archive.namelist()
        if file_name not in names:
            print(f"File not found in zip: {file_name}", file=sys.stderr)
            archive.close()
            return False

        index = names.index(file_name)
        output_file_path = output_directory + "/" + file_name
        success = self._extract_file_from_zip(archive, index, output_file_path)

        archive.close()
        return success

    def create_zip_file(self, files, output_zip_file):
        try:
            archive = zipfile.ZipFile(output_zip_file, "w")
        except Exception:
            print(f"Error opening zip file: {output_zip_file}", file=sys.stderr)
            return False

        for file_path in files:
            # maps to zip_source_file: source creation fails if file unreadable
            try:
                with open(file_path, "rb"):
                    pass
            except OSError:
                print(f"Error creating zip source for file: {file_path}", file=sys.stderr)
                archive.close()
                return False

            try:
                archive.write(file_path, arcname=file_path)
            except Exception:
                print(f"Error adding file to zip: {file_path}", file=sys.stderr)
                archive.close()
                return False

        try:
            archive.close()
        except Exception:
            print(f"Error closing zip file: {output_zip_file}", file=sys.stderr)
            return False

        return True

    def _extract_file_from_zip(self, archive, index, output_file_path):
        name = archive.namelist()[index]
        try:
            data = archive.read(name)
        except Exception:
            print(f"Failed to open file in zip: {name}", file=sys.stderr)
            return False

        try:
            out_file = open(output_file_path, "wb")
        except OSError:
            print(f"Failed to open output file: {output_file_path}", file=sys.stderr)
            return False

        try:
            out_file.write(data)
        except OSError:
            print(f"Failed to write to file: {output_file_path}", file=sys.stderr)
            out_file.close()
            return False

        out_file.close()
        return True

    def _create_directory_if_not_exists(self, dir_path):
        if not os.path.exists(dir_path):
            try:
                os.makedirs(dir_path)
                return True
            except OSError:
                return False
        return True

    def _open_zip_file(self, mode):
        try:
            return zipfile.ZipFile(self._zip_file_path, mode)
        except Exception:
            print(f"Failed to open zip file: {self._zip_file_path}", file=sys.stderr)
            return None