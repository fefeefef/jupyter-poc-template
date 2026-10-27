"""Exercise the public API used by the README quickstart."""

from project_name import greet


def test_default_greeting() -> None:
    assert greet() == "Hello, world!"


def test_named_greeting() -> None:
    assert greet("NXAI") == "Hello, NXAI!"
