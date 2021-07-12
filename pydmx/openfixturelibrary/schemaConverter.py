"""
This Module is for converting dictionaries into the according schemas.
This might add some unnecessary overhead in initialization and code complexity 
but will pay off later on due to type hinting and tracable logic.

The Logic is mainly based on the python module "dacite" in a stripped down Version
with various modifications to fit this particular usecase.
You can find more about dacite here: https://github.com/konradhalas/dacite
"""

from dataclasses import is_dataclass, _FIELDS, _FIELD, _FIELD_INITVAR, Field
from typing import (
    Any,
    Dict,
    Type,
    TypeVar,
    get_type_hints,
    List,
    Tuple,
    Optional,
    Union,
)
from copy import copy
from enum import Enum

# Specifying S as a generall Schema Variable
S = TypeVar("S")


def convert_to_schema(schema: Type[S], data: Dict[str, Any]) -> S:
    """
    """
    data_class_hints = get_type_hints(schema)
    print(data_class_hints)
    data_class_fields = get_fields(schema)
    print(data_class_fields)
    for field in data_class_fields:
        field = copy(field)
        field.type = data_class_hints[field.name]
        try:
            # The Value needs to be casted
            value = extract_value(field.type, data[field.name])
            print(value)
        except KeyError:
            pass


def extract_value(target_type: Type, value: Any) -> Any:
    """
    """
    print(f"Targettype: {target_type}")
    print(f"Value: {value}")
    # If the target type is an Enum we need to convert the value: "Ant" -> < Animal.ANT "Ant">
    try:
        if issubclass(target_type, Enum):
            # We can extract the according Enum element by querying its functional API
            value = target_type(value)
    except TypeError:
        # The issubclass function will fail when checking types and supposed to
        pass
    # Since Schemas can have Optional attributes, we assign empty ones the NoneType
    if is_optional(target_type):
        if value is None:
            return None
        # If the Value is not None we now need to extract the real type: Optional[int] -> int
        # For Optionals the NoneType is always the last one
        optional_type = target_type.__args__[0]
        return extract_value(optional_type, value)
    # Now we need to take a closer look at additional typing types: List and Dict
    # They all extend the Collection class and can therefore be filtered
    try:
        #print(f'Origin: {target_type.__origin__}')
        print(f'Extra: {target_type.__extra__}')
    except:
        pass

def get_fields(schema) -> List[Field]:
    fields = getattr(schema, _FIELDS)
    return [
        f
        for f in fields.values()
        if f._field_type is _FIELD or f._field_type is _FIELD_INITVAR
    ]


def extract_generic(type_: Type, defaults: Tuple = ()) -> tuple:
    try:
        if hasattr(type_, "_special") and type_._special:
            print(f'special {hasattr(type_, "_special")}')
            return defaults
        print(f"After Special{type_.__args__}")
        return type_.__args__ or defaults  # type: ignore
    except AttributeError:
        return defaults


def is_optional(type_: Type) -> bool:
    return is_union(type_) and type(None) in type_.__args__


def is_generic(type_: Type) -> bool:
    return hasattr(type_, "__origin__")


def is_union(type_: Type) -> bool:
    return is_generic(type_) and type_.__origin__ == Union


def extract_origin_collection(collection: Type) -> Type:
    try:
        return collection.__extra__
    except AttributeError:
        return collection.__origin__
