"""Pytest configuration and shared fixtures for directive tests."""

from docutils.core import publish_string
import pytest

from lddocutils.ldwriter import Writer


def _default_settings():
    """Return settings overrides required by LDTranslator."""
    return {
        "ld_path": "ld",
        "theme": "",
        "ld_passwords": "",
        "halt_level": 3,  # raise SystemMessage on ERROR (e.g. invalid directive options)
    }


@pytest.fixture
def publish_html():
    """Return a helper that publishes a RST string and returns the HTML."""

    def _publish(rst_source: str) -> str:
        return publish_string(
            source=rst_source,
            writer=Writer(),
            settings_overrides=_default_settings(),
        ).decode("utf-8")

    return _publish
