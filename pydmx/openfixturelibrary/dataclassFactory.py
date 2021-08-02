"""
This Module is for converting dictionaries into the according data-classes.
This will add some unnecessary overhead in initialization and code complexity 
but will prevent errors later on due to type hinting and tracable logic.

The underlying Logic is somewhat based on the python module "dacite".
You can find more about dacite here: https://github.com/konradhalas/dacite
"""

from dataclasses import MISSING, field, is_dataclass, _FIELDS, _FIELD, _FIELD_INITVAR, Field
from typing import (
    Any,
    Dict,
    Mapping,
    Type,
    TypeVar,
    get_type_hints,
    List,
    Tuple,
    Optional,
    Union,
    Collection
)
from copy import copy
from enum import Enum

#To prevent confusion with the Naming, the type which should be converted to is called Schema
Schema = TypeVar("Schema")

class typedSubclass:
    pass

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
        #Now we try to create the field
        #try:
        value = create_field(field, data[field.name])
        print(value)
        init_values[field.name] = value
        #except:
            #TODO: proper Exception Handling
            #pass
    # Creating and returning the object schema instance from the value dictionary
    #instance = schema(**init_values)
    #return instance

def create_field(field: Field, value: Any) -> Any:
    """"""
    target_type = field.type
    target_origin = None
    if hasattr(target_type, "__origin__"):
        target_origin = target_type.__origin__
    print(f'Creating: {target_type} {target_origin}')
    #First of all we might need to adjust the value e.g. if its an Enum
    # If the Type if Optional, we need to unpack the type
    if target_origin == Union and type(None) in target_type.__args__:
        print("OPT")
        if value == None:
            return None
        else:
            for type_ in target_type.__args__:
                if type_ != None:
                    field.type = type_
                    return create_field(field, value)

    # If its a value, we cast the value to the Enum value
    
    if issubclass(target_type, Enum):
        value = target_type(value)
    # List, Dict ...and issubclass(target_origin, Collection) and isinstance(value, target_origin)
    if target_origin != None :
        print("GENERIC")
        collection_cls = value.__class__
        
    return value
    #TODO: Typed Subclass


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

def is_union(type_: Type) -> bool:
    return hasattr(type_, "__origin__") and type_.__origin__ == Union

def is_instance(value: Any, type: Type) -> bool:
    """Extensive check if value equals the type

    Args:
        value (Any): Value we want to check
        type (Type): Type we want to check against

    Returns:
        bool: if it corresponds to the type
    """
    # If the type is Any, everything is valid
    if type == Any:
        return True
    # If any of the types inside the Union corresponds to the value, its valid
    elif is_union(type):
        return any(is_instance(value, t) for t in extract_generic(type))
    # Check if its a Mapping/List/Dict
    elif is_generic_collection(type):
        # By checking for the generic collection we know __origin__ exists
        origin = type.__origin__
        if not isinstance(value, origin):
            return False
        if not extract_generic(type):
            return True
        # Since Generic Collections can be multiple types we need check further
        # Tuples: not needed so far
        if isinstance(value, tuple):
            print("I WASN'T PREPARED FOR TUPLES")
        # Dicts: Typechecking every key and value
        if isinstance(value, Mapping):
            key_type, val_type = extract_generic(type, defaults=(Any, Any))
            for key, val in value.items():
                if not is_instance(key, key_type) or not is_instance(val, val_type):
                    return False
            return True
        # Lists: We iterate through and check if the items match the sepcified type
        return all(
            is_instance(item, extract_generic(type, defaults=(Any,))[0])
            for item in value
        )


def extract_generic(type_: Type, defaults: Tuple = ()) -> tuple:
    try:
        return type_.__args__ or defaults  # type: ignore
    except AttributeError:
        return defaults

def is_generic_collection(type_: Type) -> bool:
    if not hasattr(type_, "__origin__"):
        return False
    origin = type_.__origin__
    try:
        return bool(origin and issubclass(origin, Collection))
    except (TypeError, AttributeError):
        return False

def extract_origin_collection(collection: Type) -> Type:
    return collection.__origin__

class NonExceptingError(Exception):
    pass

class MissingValueError(NonExceptingError):
    def __init__(self, fieldName: str) -> None:
        super().__init__(fieldName = fieldName)
    
    def __str__(self) -> str:
        return f'missing value for field "{self.fieldName}"'

