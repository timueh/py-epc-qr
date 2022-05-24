from py_epc_qr.cli import app
from typer.testing import CliRunner
import pytest

runner = CliRunner()

def test_app_from_yaml():
    result = runner.invoke(app, ["create", "--from-yaml", "tests/data/template.yaml"])
    assert result.exit_code == 0

def test_app_from_prompt():
    result = runner.invoke(app, ["create"], input="test\nDE33100205000001194700\n10\nDanke")
    assert result.exit_code == 0

@pytest.mark.parametrize("value, expected", [
    ("$§\n", 1),
    ("hello\nDE\n", 1),
    ("hello\nDE33100205000001194700\n-10\n", 1),
    ("hello\nDE33100205000001194700\n10\n$$\n", 1),
])  
def test_app_from_prompt_throws_error(value, expected):
    result = runner.invoke(app, ["create"], input=value)
    assert result.exit_code == expected
