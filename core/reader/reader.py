from dbf import Table, READ_ONLY
from typing import Any


class Reader:

    def __init__(self, file: str):
        self.table = Table(file)
        self.table.open(mode=READ_ONLY)

    def get_table_by_index(self, posix: int) -> None:
        return self.table[posix]

    def get_table_by_criteria(self, **kwargs) -> Any:
        condition = " and ".join(
            [
                f"{k.lower()} == '{v}'" if str(v).isalnum() or str(v).isdigit()
                else f"{k.lower()} == {v}" for k, v in kwargs.items()
            ]
        )
        return self.table.query(f"SELECT * WHERE {condition}")

    def get_fields(self) -> list:
        return self.table.field_names
