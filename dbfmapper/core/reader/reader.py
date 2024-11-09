from dbf import Table, READ_ONLY
from dbfmapper.exception.exceptions import DatabaseNotFound


class Reader:

    def __init__(self, file: str) -> None:
        try:
            self.table = Table(file)
            self.table.open(mode=READ_ONLY)
        except Exception as e:
            raise DatabaseNotFound(e) from e

    def get_table_by_index(self, posix: int) -> Table:
        return self.table[posix]

    def get_table_by_criteria(self, **kwargs) -> list[Table]:
        if len(kwargs) > 0:
            condition = " and ".join(
                [
                    f"{k.lower()} == '{v}'" if str(v).isalnum() or str(v).isdigit()
                    else f"{k.lower()} == {v}" for k, v in kwargs.items()
                ]
            )
            return self.table.query(f"SELECT * WHERE {condition}")
        return

    def get_fields(self) -> list[str]:
        return self.table.field_names
