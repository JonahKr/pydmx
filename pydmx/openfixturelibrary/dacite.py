"""
This module is, as the name states, based on the module dacite: https://github.com/konradhalas/dacite
Since the OFL-Standard has some edgecases which are really unique to its design (e.g. The capability as a type in itself)
The library had to be modified a bit and is stripped down from not needed options. 
"""

import copy
from dataclasses import (
    dataclass,
    _FIELD,
    _FIELD_INITVAR,
    _FIELDS,
    MISSING,
    Field,
    InitVar,
    field,
    is_dataclass,
)
from itertools import zip_longest
from typing import (
    Callable,
    Any,
    Collection,
    Dict,
    Mapping,
    Optional,
    List,
    Set,
    Type,
    TypeVar,
    Union,
    get_type_hints,
    Tuple,
)

U = TypeVar("U")
Data = Dict[str, Any]


@dataclass
class Config:
    type_hooks: Dict[Type, Callable[[Any], Any]] = field(default_factory=dict)
    cast: List[Type] = field(default_factory=list)
    forward_references: Optional[Dict[str, Any]] = None
    check_types: bool = True
    strict: bool = False
    strict_unions_match: bool = False


def from_dict(data_class: Type[U], data: Data, config: Optional[Config] = None) -> U:
    """Create a data class instance from a dictionary.

    :param data_class: a data class type
    :param data: a dictionary of a input data
    :param config: a configuration of the creation process
    :return: an instance of a data class
    """
    init_values: Data = {}
    post_init_values: Data = {}
    config = config or Config()
    try:
        data_class_hints = get_type_hints(
            data_class, globalns=config.forward_references
        )
    except NameError as error:
        raise ForwardReferenceError(str(error))
    data_class_fields = get_fields(data_class)
    if config.strict:
        extra_fields = set(data.keys()) - {f.name for f in data_class_fields}
        if extra_fields:
            raise UnexpectedDataError(keys=extra_fields)
    for field in data_class_fields:
        field = copy.copy(field)
        field.type = data_class_hints[field.name]
        #print(f"Field Type: {field.type}")
        try:
            try:
                field_data = data[field.name]
                transformed_value = transform_value(
                    type_hooks=config.type_hooks,
                    cast=config.cast,
                    target_type=field.type,
                    value=field_data,
                )
                value = _build_value(
                    type_=field.type, data=transformed_value, config=config
                )
            except DaciteFieldError as error:
                error.update_path(field.name)
                raise
            if config.check_types and not is_instance(value, field.type):
                raise WrongTypeError(
                    field_path=field.name, field_type=field.type, value=value
                )
        except KeyError:
            try:
                value = get_default_value_for_field(field)
            except DefaultValueNotFoundError:
                if not field.init:
                    continue
                raise MissingValueError(field.name)
        if field.init:
            init_values[field.name] = value
        else:
            print("NO INIT")
            post_init_values[field.name] = value

    return create_instance(
        data_class=data_class,
        init_values=init_values,
        post_init_values=post_init_values,
    )


def _build_value(type_: Type, data: Any, config: Config) -> Any:
    if is_init_var(type_):
        type_ = extract_init_var(type_)
    if is_union(type_):
        return _build_value_for_union(union=type_, data=data, config=config)
    elif is_generic_collection(type_) and is_instance(
        data, extract_origin_collection(type_)
    ):
        return _build_value_for_collection(collection=type_, data=data, config=config)
    elif is_dataclass(type_) and is_instance(data, Data):
        return from_dict(data_class=type_, data=data, config=config)
    return data


def _build_value_for_union(union: Type, data: Any, config: Config) -> Any:
    types = extract_generic(union)
    if is_optional(union) and len(types) == 2:
        return _build_value(type_=types[0], data=data, config=config)
    union_matches = {}
    for inner_type in types:
        try:
            # noinspection PyBroadException
            try:
                data = transform_value(
                    type_hooks=config.type_hooks,
                    cast=config.cast,
                    target_type=inner_type,
                    value=data,
                )
            except Exception:  # pylint: disable=broad-except
                continue
            value = _build_value(type_=inner_type, data=data, config=config)
            if is_instance(value, inner_type):
                if config.strict_unions_match:
                    union_matches[inner_type] = value
                else:
                    return value
        except DaciteError:
            pass
    if config.strict_unions_match:
        if len(union_matches) > 1:
            raise StrictUnionMatchError(union_matches)
        return union_matches.popitem()[1]
    if not config.check_types:
        return data
    raise UnionMatchError(field_type=union, value=data)


def _build_value_for_collection(collection: Type, data: Any, config: Config) -> Any:
    data_type = data.__class__
    if is_instance(data, Mapping):
        item_type = extract_generic(collection, defaults=(Any, Any))[1]
        return data_type(
            (key, _build_value(type_=item_type, data=value, config=config))
            for key, value in data.items()
        )
    elif is_instance(data, tuple):
        types = extract_generic(collection)
        if len(types) == 2 and types[1] == Ellipsis:
            return data_type(
                _build_value(type_=types[0], data=item, config=config) for item in data
            )
        return data_type(
            _build_value(type_=type_, data=item, config=config)
            for item, type_ in zip_longest(data, types)
        )
    item_type = extract_generic(collection, defaults=(Any,))[0]
    return data_type(
        _build_value(type_=item_type, data=item, config=config) for item in data
    )


T = TypeVar("T", bound=Any)


class DefaultValueNotFoundError(Exception):
    pass


def get_default_value_for_field(field: Field) -> Any:
    if field.default != MISSING:
        return field.default
    elif field.default_factory != MISSING:  # type: ignore
        return field.default_factory()  # type: ignore
    elif is_optional(field.type):
        return None
    raise DefaultValueNotFoundError()


def create_instance(
    data_class: Type[T], init_values: Data, post_init_values: Data
) -> T:
    instance = data_class(**init_values)
    for key, value in post_init_values.items():
        setattr(instance, key, value)
    return instance


def get_fields(data_class: Type[T]) -> List[Field]:
    fields = getattr(data_class, _FIELDS)
    return [
        f
        for f in fields.values()
        if f._field_type is _FIELD or f._field_type is _FIELD_INITVAR
    ]


def transform_value(
    type_hooks: Dict[Type, Callable[[Any], Any]],
    cast: List[Type],
    target_type: Type,
    value: Any,
) -> Any:
    print(f'Creating: {target_type}')
    if target_type in type_hooks:
        value = type_hooks[target_type](value)
    else:
        for cast_type in cast:
            print(f'Cast: {cast_type} {target_type}')
            if is_subclass(target_type, cast_type):
                if is_generic_collection(target_type):
                    value = extract_origin_collection(target_type)(value)
                else:
                    value = target_type(value)
                break
    if is_optional(target_type):
        if value is None:
            return None
        target_type = extract_optional(target_type)
        print("RECURSIVE TRANS")
        return transform_value(type_hooks, cast, target_type, value)
    if is_generic_collection(target_type) and isinstance(
        value, extract_origin_collection(target_type)
    ):
        print(f"GENERIC IDENTIFIED {target_type}")
        collection_cls = value.__class__
        if issubclass(collection_cls, dict):
            key_cls, item_cls = extract_generic(target_type, defaults=(Any, Any))
            return collection_cls(
                {
                    transform_value(type_hooks, cast, key_cls, key): transform_value(
                        type_hooks, cast, item_cls, item
                    )
                    for key, item in value.items()
                }
            )
        item_cls = extract_generic(target_type, defaults=(Any,))[0]
        return collection_cls(
            transform_value(type_hooks, cast, item_cls, item) for item in value
        )
    return value


def extract_origin_collection(collection: Type) -> Type:
    try:
        return collection.__extra__
    except AttributeError:
        return collection.__origin__


def is_optional(type_: Type) -> bool:
    return is_union(type_) and type(None) in extract_generic(type_)


def extract_optional(optional: Type[Optional[T]]) -> T:
    for type_ in extract_generic(optional):
        if type_ is not type(None):
            return type_
    raise ValueError("can not find not-none value")


def is_generic(type_: Type) -> bool:
    return hasattr(type_, "__origin__")


def is_union(type_: Type) -> bool:
    return is_generic(type_) and type_.__origin__ == Union


def is_literal(type_: Type) -> bool:
    try:
        from typing import Literal  # type: ignore

        return is_generic(type_) and type_.__origin__ == Literal
    except ImportError:
        return False


def is_new_type(type_: Type) -> bool:
    return hasattr(type_, "__supertype__")


def extract_new_type(type_: Type) -> Type:
    return type_.__supertype__


def is_init_var(type_: Type) -> bool:
    return isinstance(type_, InitVar) or type_ is InitVar


def extract_init_var(type_: Type) -> Union[Type, Any]:
    try:
        return type_.type
    except AttributeError:
        return Any


def is_instance(value: Any, type_: Type) -> bool:
    if type_ == Any:
        return True
    elif is_union(type_):
        return any(is_instance(value, t) for t in extract_generic(type_))
    elif is_generic_collection(type_):
        #print(f"Generic COllection of type: {type_} and value {value}")
        origin = extract_origin_collection(type_)
        if not isinstance(value, origin):
            #print("F1")
            return False
        if not extract_generic(type_):
            return True
        if isinstance(value, tuple):
            #print("TUPLE!")
            tuple_types = extract_generic(type_)
            if len(tuple_types) == 1 and tuple_types[0] == ():
                #print("Special Tuple")
                return len(value) == 0
            elif len(tuple_types) == 2 and tuple_types[1] is ...:
                #print("TUPLE")
                return all(is_instance(item, tuple_types[0]) for item in value)
            else:
                if len(tuple_types) != len(value):
                    #print("F2")
                    return False
                return all(
                    is_instance(item, item_type)
                    for item, item_type in zip(value, tuple_types)
                )
        if isinstance(value, Mapping):
            key_type, val_type = extract_generic(type_, defaults=(Any, Any))
            for key, val in value.items():
                if not is_instance(key, key_type) or not is_instance(val, val_type):
                    #print("F3")
                    return False
            return True
        return all(
            is_instance(item, extract_generic(type_, defaults=(Any,))[0])
            for item in value
        )
    elif is_new_type(type_):
        return is_instance(value, extract_new_type(type_))
    elif is_literal(type_):
        return value in extract_generic(type_)
    elif is_init_var(type_):
        return is_instance(value, extract_init_var(type_))
    elif is_type_generic(type_):
        return is_subclass(value, extract_generic(type_)[0])
    else:
        try:
            # As described in PEP 484 - section: "The numeric tower"
            if isinstance(value, (int, float)) and type_ in [float, complex]:
                return True
            return isinstance(value, type_)
        except TypeError:
            #print("F4")
            return False


def is_generic_collection(type_: Type) -> bool:
    if not is_generic(type_):
        return False
    origin = extract_origin_collection(type_)
    try:
        return bool(origin and issubclass(origin, Collection))
    except (TypeError, AttributeError):
        return False


def extract_generic(type_: Type, defaults: Tuple = ()) -> tuple:
    try:
        if hasattr(type_, "_special") and type_._special:
            #print("GENERICA EXTRACTA")
            return defaults
        return type_.__args__ or defaults  # type: ignore
    except AttributeError:
        return defaults


def is_subclass(sub_type: Type, base_type: Type) -> bool:
    if is_generic_collection(sub_type):
        print("GENERIC SUB")
        sub_type = extract_origin_collection(sub_type)
        print(sub_type)
    try:
        return issubclass(sub_type, base_type)
    except TypeError:
        return False


def is_type_generic(type_: Type) -> bool:
    try:
        return type_.__origin__ in (type, Type)
    except AttributeError:
        return False


def _name(type_: Type) -> str:
    return type_.__name__ if hasattr(type_, "__name__") else str(type_)


class DaciteError(Exception):
    pass


class DaciteFieldError(DaciteError):
    def __init__(self, field_path: Optional[str] = None):
        super().__init__()
        self.field_path = field_path

    def update_path(self, parent_field_path: str) -> None:
        if self.field_path:
            self.field_path = f"{parent_field_path}.{self.field_path}"
        else:
            self.field_path = parent_field_path


class WrongTypeError(DaciteFieldError):
    def __init__(
        self, field_type: Type, value: Any, field_path: Optional[str] = None
    ) -> None:
        super().__init__(field_path=field_path)
        self.field_type = field_type
        self.value = value

    def __str__(self) -> str:
        return (
            f'wrong value type for field "{self.field_path}" - should be "{_name(self.field_type)}" '
            f'instead of value "{self.value}" of type "{_name(type(self.value))}"'
        )


class MissingValueError(DaciteFieldError):
    def __init__(self, field_path: Optional[str] = None):
        super().__init__(field_path=field_path)

    def __str__(self) -> str:
        return f'missing value for field "{self.field_path}"'


class UnionMatchError(WrongTypeError):
    def __str__(self) -> str:
        return (
            f'can not match type "{_name(type(self.value))}" to any type '
            f'of "{self.field_path}" union: {_name(self.field_type)}'
        )


class StrictUnionMatchError(DaciteFieldError):
    def __init__(
        self, union_matches: Dict[Type, Any], field_path: Optional[str] = None
    ) -> None:
        super().__init__(field_path=field_path)
        self.union_matches = union_matches

    def __str__(self) -> str:
        conflicting_types = ", ".join(_name(type_) for type_ in self.union_matches)
        return f'can not choose between possible Union matches for field "{self.field_path}": {conflicting_types}'


class ForwardReferenceError(DaciteError):
    def __init__(self, message: str) -> None:
        super().__init__()
        self.message = message

    def __str__(self) -> str:
        return f"can not resolve forward reference: {self.message}"


class UnexpectedDataError(DaciteError):
    def __init__(self, keys: Set[str]) -> None:
        super().__init__()
        self.keys = keys

    def __str__(self) -> str:
        formatted_keys = ", ".join(f'"{key}"' for key in self.keys)
        return f"can not match {formatted_keys} to any data class field"
