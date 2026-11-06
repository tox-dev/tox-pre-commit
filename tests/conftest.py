"""Pytest configuration for the test suite."""

from __future__ import annotations

import os
import typing as _t

import pytest


if _t.TYPE_CHECKING:
    from collections import abc as _c  # noqa: WPS347


pytest_plugins = ('tox.pytest',)


@pytest.fixture
def _isolate_user_environment() -> _c.Iterator[None]:
    """Isolate the tests from the user's tox configuration.

    :yields: Control to the test while the user configuration is hidden.
    """
    # `usefixtures` starts this before tox's environment check, so its own
    # monkeypatch must outlive that check rather than share the test's one
    with pytest.MonkeyPatch.context() as monkeypatch:
        monkeypatch.setenv('TOX_USER_CONFIG_FILE', os.devnull)
        yield
