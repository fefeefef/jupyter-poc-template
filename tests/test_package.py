"""Exercise the public API used by the README quickstart."""

from project_name import greet


def test_greeting() -> None:
    assert greet() == "hello"
