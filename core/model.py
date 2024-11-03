from typing import Annotated
from .base.base_model import BaseModel
from .reader.reader import Reader
from typing import get_origin


class Model(BaseModel):

    def __init__(self, subclass: object = None) -> None:
        self.subclass = subclass
        self.reader = Reader(self.subclass.__ctx__)

    def __find_relationships(self) -> None:
        for subclass in Model.__subclasses__():
            if subclass.__name__ != self.subclass.__class__.__name__:
                instance = subclass()

                for k, v in instance.__dict__.items():
                    if get_origin(v) == Annotated:
                        metadata = v.__dict__["__metadata__"]

                        for rel in metadata[0]["foreign_key"]:
                            if rel.__name__ == self.subclass.__class__.__name__:
                                if hasattr(self.subclass, k):
                                    condition = {str(k): getattr(self.subclass, k)}
                                    setattr(
                                        self.subclass,
                                        instance.__class__.__name__.upper(),
                                        instance.get_all(**condition, easy_view=True)
                                    )

    def get(self, **kwargs) -> None:
        result: list = self.reader.get_table_by_criteria(**kwargs)

        if len(result) > 0:
            for i, k in enumerate(self.reader.get_fields()):
                if hasattr(self, k):
                    setattr(self, k, str(result[0][i]).strip())
            self.__find_relationships()
        else:
            raise Exception("Table not found by criteria")

    def get_all(self, easy_view=False, **kwargs) -> list:
        result: list = self.reader.get_table_by_criteria(**kwargs)
        object_list: list = []

        for record in result:
            new_object = type(self.subclass)()

            for i, k in enumerate(self.reader.get_fields()):
                if hasattr(new_object, k):
                    setattr(new_object, k, str(record[i]).strip())
            object_list.append(
                new_object.to_repr() if easy_view else new_object
            )

        return object_list

    def join(self, **kwargs) -> None:
        ...

    def relate(self, **kwargs) -> None:
        ...

    def __add__(self, other):
        new_repr = self.to_repr()
        new_repr[other.__class__.__name__] = other.to_repr()
        return new_repr

    def to_repr(self) -> dict:
        repr_dict = {}

        for k, v in self.subclass.__dict__.items():
            if isinstance(v, type(self.subclass)) is False:
                repr_dict[k] = v
        repr_dict.pop("reader")

        return repr_dict
