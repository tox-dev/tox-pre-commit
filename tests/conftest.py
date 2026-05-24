"""Pytest configuration for the test suite."""

from __future__ import annotations

import os

import pytest


pytest_plugins = ('tox.pytest',)


@pytest.fixture(autouse=True)
def _isolate_user_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    """Isolate the tests from the user's tox configuration.

    :param monkeypatch: Pytest's environment-manipulation fixture.
    """
    monkeypatch.setenv('TOX_USER_CONFIG_FILE', os.devnull)
