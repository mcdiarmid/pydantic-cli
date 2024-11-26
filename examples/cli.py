from pydantic import Field

from pydantic_cli import CliBase


class CliTest(CliBase):
    """This is a CLI program defined with Pydantic models."""
    foo: str
    bar: int
    baz: bool = False
    boz: bool = Field(default_factory=lambda: True)


if __name__ == "__main__":
    args = CliTest.parse_args()
    print(repr(args))
