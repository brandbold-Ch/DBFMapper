from typing import Annotated, get_origin, Any, TypeVar, Type, Generic
from .core.base.base_model import BaseModel
from .exception.exceptions import NotFoundTable, InvalidAnnotatedType, DBFException
from .core.reader.reader import Reader
from enum import Enum

T = TypeVar('T', bound=BaseModel)


class Model(Generic[T]):
    """
    A generic class that manages model data and relationships.
    It allows for querying the model, fetching related entities, and
    representing the model's data in a dictionary format.

    Attributes:
        subclass (Type[T]): The specific subclass type of the model.
        reader (Reader): A reader object to interact with the model's data.
    """

    def __new__(cls, *args, **kwargs):
        """
        Creates a new instance of the Model class and binds it to its specific subclass.

        This method ensures that the `T` type is dynamically set with the appropriate
        subclass during initialization.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            object: A new instance of the Model class.
        """
        subclasses = Model.__subclasses__()
        if cls in subclasses:
            ctx_type = subclasses[subclasses.index(cls)]
            T.__setattr__("__bound__", ctx_type)
        return super().__new__(cls)

    def __init__(self, subclass: Type[T]) -> None:
        """
        Initializes the model with a specific subclass and sets up the reader
        for querying the data related to that subclass.

        Args:
            subclass (Type[T]): The specific subclass type of the model.
        """
        self.subclass = subclass
        self.reader = Reader(subclass.__ctx__)

    def _subclasses(self) -> list[T]:
        """
        Returns a list of all subclasses of the Model class.

        This helper method allows us to discover all possible subclasses that extend
        the base Model class.

        Returns:
            list[T]: A list of subclasses.
        """
        return Model.__subclasses__()

    def _subclass_name(self) -> str:
        """
        Returns the name of the subclass for the current model instance.

        This method retrieves the name of the subclass to use in relationships
        or metadata manipulations.

        Returns:
            str: The name of the subclass.
        """
        return self.subclass.__class__.__name__

    def _subclass_meta(self, var) -> tuple[dict]:
        """
        Extracts the metadata of an annotated field in the model.

        This method ensures that the field is of the correct type (`Annotated`) and
        retrieves the associated metadata.

        Args:
            var: The variable representing the annotated field.

        Returns:
            tuple[dict]: The metadata dictionary for the annotated field.

        Raises:
            Exception: If the variable is not of type `Annotated`.
        """
        if get_origin(var) != Annotated:
            raise InvalidAnnotatedType("Invalid Type: Must be Annotated type.")
        return var.__dict__["__metadata__"]

    def _find_relationships(self) -> None:
        """
        Finds and establishes relationships between the current model and its subclasses.

        This method looks for foreign key relationships and assigns related data to
        the current model instance based on subclass metadata.

        It uses the `Annotated` type to identify and process foreign key relationships.

        Raises:
            Exception: If there are issues with finding relationships.
        """
        try:
            for subclass in self._subclasses():
                if subclass.__name__ != self._subclass_name():
                    instance = subclass()

                    for k, v in instance.__dict__.items():
                        if get_origin(v) == Annotated:
                            metadata = self._subclass_meta(v)

                            for rel in metadata[0]["foreign_key"]:
                                if rel.__name__ == self._subclass_name():
                                    if hasattr(self.subclass, k):
                                        condition = {str(k): getattr(self.subclass, k)}
                                        setattr(
                                            self.subclass,
                                            instance._subclass_name(),
                                            instance.get_all(**condition, easy_view=True)
                                        )
        except Exception as e:
            raise DBFException(e)

    def get(self, relates: bool = False, **kwargs) -> T:
        """
        Retrieves a single instance of the model based on provided criteria.

        This method queries the model using the `Reader` and sets the attributes
        of the model instance based on the query results. If relationships are
        required, it will also fetch and set related data.

        Args:
            relates (bool): Whether to fetch related data (default is False).
            **kwargs: Query parameters used to filter the results.

        Returns:
            T: The subclass model instance with the queried data.

        Raises:
            Exception: If no results are found based on the criteria.
        """
        result: list = self.reader.get_table_by_criteria(**kwargs)

        if len(result) > 0:
            for i, k in enumerate(self.reader.get_fields()):
                if hasattr(self, k):
                    setattr(self, k, str(result[0][i]).strip())

            if relates:
                self._find_relationships()
        else:
            raise NotFoundTable("Table not found by criteria.")
        return self.subclass

    def get_all(self, easy_view: bool = False, **kwargs) -> list[T] | list[dict]:
        """
        Retrieves all instances of the model based on provided criteria.

        This method queries the model using the `Reader` and returns a list of
        instances. Each instance can either be a full model object or a simplified
        dictionary representation, depending on the `easy_view` flag.

        Args:
            easy_view (bool): Whether to return a simplified dictionary view (default is False).
            **kwargs: Query parameters used to filter the results.

        Returns:
            list[T] | list[dict]: A list of model instances or simplified dictionary representations.
        """
        try:
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
        except Exception as e:
            raise DBFException(e)

    def __add__(self, other: T):
        """
        Adds another model instance's representation to the current model instance's representation.

        This method merges the representation of another model instance (`other`) into
        the current model's dictionary representation.

        Args:
            other (T): Another model instance to add.

        Returns:
            dict: A dictionary representation of the merged model data.
        """
        try:
            new_repr = self.to_repr()
            new_repr[other.__class__.__name__] = other.to_repr()
            return new_repr
        except Exception:
            raise DBFException("Error getting data")

    def to_repr(self) -> dict:
        """
        Converts the model instance to a dictionary representation.

        This method generates a dictionary of the model instance's attributes, excluding
        the `reader` attribute and any relationships.

        Returns:
            dict: A dictionary representation of the model instance.
        """
        try:
            repr_dict = {}

            for k, v in self.subclass.__dict__.items():
                if isinstance(v, type(self.subclass)) is False:
                    repr_dict[k] = v
            repr_dict.pop("reader")

            return repr_dict
        except Exception:
            raise DBFException("Error in data introspection")
