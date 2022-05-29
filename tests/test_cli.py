"""
Tests for the cli.
"""

import pytest
from typer.testing import CliRunner

from py_epc_qr import __version__
from py_epc_qr.cli import app

runner = CliRunner()


def test_app_from_yaml():
    """
    Given a yaml template
    When creating the QR code
    Then everything works as intended
    """
    result = runner.invoke(app, ["create", "--from-yaml", "tests/data/template.yaml"])
    assert result.exit_code == 0


def test_app_from_prompt():
    """
    Given a valid prompt input
    When creating the QR code
    Then everything works as intended
    """
    result = runner.invoke(
        app, ["create"], input="test\nDE33100205000001194700\n10\nDanke"
    )
    assert result.exit_code == 0


@pytest.mark.parametrize(
    "value, expected",
    [
        ("$§\n", 1),
        ("hello\nDE\n", 1),
        ("hello\nDE33100205000001194700\n-10\n", 1),
        ("hello\nDE33100205000001194700\n10\n$$\n", 1),
    ],
)
def test_app_from_prompt_throws_error(value, expected):
    """
    Given invalid prompt inputs
    When creating the QR code
    Then an expected return code is thrown
    """
    result = runner.invoke(app, ["create"], input=value)
    assert result.exit_code == expected


def test_app_version():
    """
    Given the version command
    When invoking it
    Then the version is printed correctly
    """
    result = runner.invoke(app, ["version"])
    assert result.stdout == f"py-epc-qr v{__version__}\n"
    assert result.exit_code == 0
