import csv
from pathlib import Path

from definitions import ROOT_DIR


class CsvParser:
    """CSV Parser"""
    _root: Path = ROOT_DIR / Path(r'doc')
    csv_file_name: str = ''

    load_list: list[dict[str, str]]
    headers: list[str]

    @classmethod
    @property
    def path(cls) -> Path:
        """Path"""
        return cls._root / cls.csv_file_name

    @classmethod
    def load_data(cls) -> None:
        """Load data from .lua and convert to dictionary"""
        with open(cls.path, "r", encoding="utf8") as file:
            reader = csv.reader(file, delimiter="|", skipinitialspace=True)
            cls.headers = next(reader)
            cls.load_list = [dict(zip(cls.headers, row)) for row in reader]
