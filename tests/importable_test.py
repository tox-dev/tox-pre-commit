"""Smoke tests related to loading entry points."""

from dataclasses import dataclass
from importlib.metadata import entry_points as _discover_entry_points

import pytest


@dataclass(frozen=True)
class EntryPointParam:
    """Data structure representing a single exposed plugin."""

    group: str
    name: str
    spec: str

    def __str__(self) -> str:
        """Render an entry-point parameter as a string.

        To be used as a part of parametrized test ID.
        """
        return f'{self.name}={self.spec}@{self.group}'


tox_plugin_entry_points = (
    EntryPointParam(
        'tox',
        'tox-pre-commit',
        'tox_plugins.pre_commit._plugin',
    ),
)


with_tox_plugins = pytest.mark.parametrize(
    'entry_point',
    tox_plugin_entry_points,
    ids=str,
)


@with_tox_plugins
def test_entry_points_exposed(entry_point: EntryPointParam) -> None:
    """Verify the plugin entry points are discoverable.

    This check relies on the plugin-declaring distribution package to be
    pre-installed.
    """
    entry_points = _discover_entry_points(group=entry_point.group)

    assert entry_point.name in entry_points.names
    assert entry_points[entry_point.name].value == entry_point.spec
