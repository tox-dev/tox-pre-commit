"""This module exists to validate that the skeleton is functional.

It can be deleted once the project has actual tests in.
"""

from tox_plugins.pre_commit import _plugin


def test_smoke() -> None:
    """Ensure the CI picks this up."""
    assert _plugin
