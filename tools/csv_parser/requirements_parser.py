from dataclasses import dataclass
from typing import Optional

from tools.csv_parser.csv_parser import CsvParser


@dataclass
class Requirements:
    FRS_TESO_FISHER_010000: str
    FRS_TESO_FISHER_010100: str
    FRS_TESO_FISHER_010101: str
    FRS_TESO_FISHER_010102: str
    FRS_TESO_FISHER_010103: str


class RequirementsParser(CsvParser):
    """Requirements Parser"""
    csv_file_name: str = 'requirements.csv'
    requirements: Optional[dict[str, str]] = None

    @classmethod
    def load_data(cls) -> None:
        super(RequirementsParser, cls).load_data()
        cls.set_requirements()

    @classmethod
    def set_requirements(cls) -> None:
        for row in cls.load_list:
            requirement = row.get('requirement')
            description = row.get('description')
            if requirement in Requirements.__annotations__.keys():
                setattr(Requirements, requirement, description)

