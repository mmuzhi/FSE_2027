import logging
import zipfile
from pathlib import Path

logger = logging.getLogger(__name__)


class ZipFileProcessor:

    def __init__(self, zipFileName):
        self.zipFilePath = Path(zipFileName)

    def readZipFile(self):
        if not self.zipFilePath.exists():
            logger.error("Zip file does not exist: " + str(self.zipFilePath.resolve()))
            return None
        try:
            return zipfile.ZipFile(str(self.zipFilePath), 'r')
        except (OSError, zipfile.BadZipFile) as e:
            logger.error("Failed to read the zip file: " + str(self.zipFilePath.resolve()), exc_info=e)
            return None

    def extractAll(self, outputDir):
        outputDirPath = Path(outputDir)
        zipFile = self.readZipFile()
        if zipFile is None:
            return False
        try:
            if not outputDirPath.exists():
                try:
                    outputDirPath.mkdir(parents=True, exist_ok=True)
                    logger.info("Created output directory: " + str(outputDirPath.resolve()))
                except OSError as e:
                    logger.error("Failed to create output directory: " + str(outputDirPath.resolve()), exc_info=e)
                    return False

            for entry in zipFile.infolist():
                filePath = outputDirPath / entry.filename
                try:
                    if entry.is_dir():
                        if not filePath.exists():
                            filePath.mkdir(parents=True, exist_ok=True)
                            logger.info("Created directory: " + str(filePath.resolve()))
                    else:
                        with zipFile.open(entry) as inStream:
                            with open(filePath, 'wb') as outStream:
                                while True:
                                    buffer = inStream.read(1024)
                                    if not buffer:
                                        break
                                    outStream.write(buffer)
                        logger.info("Extracted file: " + str(filePath.resolve()))
                except (OSError, zipfile.BadZipFile) as e:
                    logger.error("Failed to process entry: " + entry.filename, exc_info=e)

            return True
        except (OSError, zipfile.BadZipFile) as e:
            logger.error("Failed to extract files from zip: " + str(self.zipFilePath.resolve()), exc_info=e)
            return False
        finally:
            zipFile.close()

    def extractFile(self, fileName, outputDir):
        outputDirPath = Path(outputDir)
        filePath = outputDirPath / fileName
        zipFile = self.readZipFile()
        if zipFile is None:
            return False
        try:
            try:
                entry = zipFile.getinfo(fileName)
            except KeyError:
                entry = None
            if entry is None:
                logger.warning("File not found in zip: " + fileName)
                return False

            if not filePath.parent.exists():
                try:
                    filePath.parent.mkdir(parents=True, exist_ok=True)
                    logger.info("Created parent directory: " + str(filePath.parent.resolve()))
                except OSError as e:
                    logger.error("Failed to create parent directory: " + str(filePath.parent.resolve()), exc_info=e)
                    return False

            if entry.is_dir():
                if not filePath.exists():
                    filePath.mkdir(parents=True, exist_ok=True)
                    logger.info("Created directory: " + str(filePath.resolve()))
            else:
                with zipFile.open(entry) as inStream:
                    with open(filePath, 'wb') as outStream:
                        while True:
                            buffer = inStream.read(1024)
                            if not buffer:
                                break
                            outStream.write(buffer)
                logger.info("Extracted file: " + str(filePath.resolve()))

            return True
        except (OSError, zipfile.BadZipFile) as e:
            logger.error("Failed to extract file: " + fileName, exc_info=e)
            return False
        finally:
            zipFile.close()