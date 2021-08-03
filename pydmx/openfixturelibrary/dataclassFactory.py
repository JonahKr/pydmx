"""
This Module is for converting dictionaries into the according data-classes.
This will add some unnecessary overhead in initialization and code complexity 
but will prevent errors later on due to type hinting and tracable logic.

The underlying Logic is somewhat based on the python module "dacite" (MIT-License).
You can find more about dacite here: https://github.com/konradhalas/dacite
"""

from copy import copy
from dataclasses import (
    _FIELD,
    _FIELD_INITVAR,
    _FIELDS,
    MISSING,
    is_dataclass,
)
from enum import Enum
from typing import (
    Any,
    Collection,
    Dict,
    Optional,
    Type,
    TypeVar,
    Union,
    get_type_hints,
)

# To prevent confusion with the Naming, the type which should be converted to is called Schema
Schema = TypeVar("Schema")


def create_from_dict(schema: Type[Schema], data: Dict[str, Any]) -> Schema:
    """Creating a dataclass object based on a schema and a dictionary with Enum conversion.
        It supports Enum conversion, typedSubclasses ,...
    Args:
        schema (Type[Schema]): Schema/Dataclass which should be created
        data (Dict[str, Any]): data to be converted from

    Returns:
        Schema: An object of the Schema
    """
    # Fetching a dict of all attributes of the schema and the according types
    data_class_hints = get_type_hints(schema)
    # Fetching a list of fields of the dataclass
    data_class_fields = [
        f
        for f in getattr(schema, _FIELDS).values()
        if f._field_type is _FIELD or f._field_type is _FIELD_INITVAR
    ]
    # Dictionary to keep track of all the field values of Schema
    init_values: Dict[str, Any] = {}

    # Now we need to loop through all fields and try to adjust the data + create the values
    for field in data_class_fields:
        # Creating a shallow copy of the current field
        field = copy(field)
        field.type = data_class_hints[field.name]
        # Now we try to create the field
        try:
            value = create_type_value(field.type, data[field.name])
        except NoMatchingTypeError:
            print("The value doesn't fit the required type!")
        # A Keyerror will occur if data has no field.name key aka is undefined
        except KeyError:
            value = None

        # In the case that the Schema already has a preset value for the field,
        # We check if the created value equals the set value and raise incase not.
        if field.default != MISSING and value != field.default:
            raise NoMatchingTypeError(field.type, value)
        # print(value)
        init_values[field.name] = value

    # Creating and returning the object schema instance from the value dictionary
    instance = schema(**init_values)
    return instance


def create_type_value(target_type: Type, value: Any) -> Any:
    """This Creates the value to a sepcific type.

    Args:
        target_type (Type): The type to try create the value from
        value (Any): The value to be transformed / type approved

    Raises:
        NoMatchingTypeError: If no type fits to the value

    Returns:
        Any: the value to the specific type
    """
    target_origin = None
    if hasattr(target_type, "__origin__"):
        target_origin = target_type.__origin__
    target_args = ()
    if hasattr(target_type, "__args__"):
        target_args = target_type.__args__

    # Type Any means anything can be right
    if target_type == Any:
        return value
    # If its a Union we need to unpack the types
    elif target_origin == Union:
        # Optional is a specific subtype of a Union including None
        if type(None) in target_args and value == None:
            return None
        # We just try to create the value for every type in the Union
        for type_ in target_args:
            if type_ != None:
                try:
                    return create_type_value(type_, value)
                except NoMatchingTypeError:
                    continue
        # If no type fits the value, we
        raise NoMatchingTypeError(target_type, value)
    # List, Dict
    elif (
        target_origin != None
        and issubclass(target_origin, Collection)
        and isinstance(value, target_origin)
    ):
        # The Class of the Collection: <class 'list'> or <class 'dict'>
        collection_class = value.__class__
        if issubclass(collection_class, dict):
            key_type, item_type = target_type.__args__
            # Here we create a dictionary with the key, item pairs
            return collection_class(
                {
                    create_type_value(key_type, key): create_type_value(item_type, item)
                    for key, item in value.items()
                }
            )
        # The second case is the list in which case we create the value for every item
        item_class = target_args[0] or Any
        return collection_class(create_type_value(item_class, item) for item in value)
    # If the type is an Enum, we cast the value
    elif issubclass(target_type, Enum):
        return target_type(value)
    # Dataclass
    elif is_dataclass(target_type):
        return create_from_dict(target_type, value)
    # Everything else: str, int ...
    elif isinstance(value, target_type):
        return value
    # If we got until here, no appropriate match was found
    raise NoMatchingTypeError(target_type, value)


class NoMatchingTypeError(Exception):
    def __init__(self, type_: Any, value: Any) -> None:
        self.type_ = type_
        self.value = value

    def __str__(self) -> str:
        return f"Type {self.type} didn't match the value {self.value}"
