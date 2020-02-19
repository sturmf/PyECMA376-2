import zipfile
from typing import Iterable, BinaryIO, IO

from . import package_model

CONTENT_TYPES_STREAM_NAME = "/[ContentTypes.xml]"


class ZipPackageReader(package_model.OPCPackageReader, zipfile.ZipFile):
    content_types_stream_name = CONTENT_TYPES_STREAM_NAME

    def __init__(self, file):
        package_model.OPCPackageReader.__init__(self)
        zipfile.ZipFile.__init__(self, file)

        # Read content types data
        with self.open_part(""):
            self.content_types = package_model.ContentTypesData.from_xml()

    def list_items(self) -> Iterable[str]:
        return ["/" + name for name in self.namelist()]

    def open_item(self, name: str) -> IO[bytes]:
        return self.open(name[1:])

    def close(self) -> None:
        zipfile.ZipFile.close(self)


class ZipPackageWriter(package_model.OPCPackageWriter, zipfile.ZipFile):
    content_types_stream_name = CONTENT_TYPES_STREAM_NAME

    def __init__(self, file):
        package_model.OPCPackageWriter.__init__(self)
        zipfile.ZipFile.__init__(self, file, mode='w')

    def close(self) -> None:
        package_model.OPCPackageWriter.close(self)
        zipfile.ZipFile.close(self)

    def create_item(self, name: str, content_type: str) -> IO[bytes]:
        return self.open(name[1:], mode='w')
