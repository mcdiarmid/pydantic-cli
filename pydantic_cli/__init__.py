from argparse import ArgumentParser
from typing import Any

from typing_extensions import Self
from pydantic import BaseModel
from pydantic.fields import Field, FieldInfo
from pydantic_core import PydanticUndefined


def get_field_parser_kwargs(info: FieldInfo) -> dict[str, Any]:
    """Generates kwargs of an annotated field for a new ArgumentParser argument.

    Args:
        info (FieldInfo): Information for an annotated field of a Pydantic model.

    Returns:
        dict of kwargs for ArgumentParser.add_argument(...)
    """
    kwargs = {}
    default = info.default_factory() if info.default_factory else info.default
    if default not in (PydanticUndefined, None):
        kwargs.update(required=info.is_required(), default=default)

    if issubclass(info.annotation, bool):
        kwargs.update(action='store_false' if default is True else 'store_true')
    elif issubclass(info.annotation, list | tuple):  # Nargs?
        raise NotImplementedError
    else:
        kwargs.update(type=str)  # Let pydantic do casting & validation

    return kwargs


class CliBase(BaseModel):
    @classmethod
    def parse_args(cls: type[Self]) -> Self:
        parser = ArgumentParser(
            exit_on_error=False,
            description=cls.__doc__,
        )
        for arg, info in cls.model_fields.items():
            parser.add_argument(
                arg if info.is_required() else f'--{arg}',
                help=info.description,
                **get_field_parser_kwargs(info),
            )
        ns = parser.parse_args()
        return cls.model_validate(ns.__dict__)
