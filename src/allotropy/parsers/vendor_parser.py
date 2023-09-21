from abc import ABC, abstractmethod
import io
from typing import Any, Optional

import chardet

from allotropy.allotrope.allotrope import AllotropeConversionError
from allotropy.parsers.utils.timestamp_parser import TimestampParser


class VendorParser(ABC):
    def __init__(self, timestamp_parser: TimestampParser):
        self.timestamp_parser = timestamp_parser

    @abstractmethod
    def _parse(self, contents: io.IOBase, filename: str) -> Any:
        raise NotImplementedError

    def to_allotrope(self, contents: io.IOBase, filename: str) -> Any:
        return self._parse(contents, filename)

    def _read_contents(self, contents: io.IOBase) -> Any:
        file_bytes = contents.read()
        encoding = chardet.detect(file_bytes)["encoding"]
        if not encoding:
            error = "Did not detect encoding in input file"
            raise AllotropeConversionError(error)
        return file_bytes.decode(encoding)

    def parse_timestamp(self, time: Optional[str]) -> Optional[str]:
        return self.timestamp_parser.parse(time)
