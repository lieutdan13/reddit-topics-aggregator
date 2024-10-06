import pytest
from unittest.mock import patch, mock_open
from reddit_topics_aggregator.package_metadata import (
    get_package_metadata,
    get_package_name,
    get_package_version,
)

# Sample valid pyproject.toml content
valid_toml_content = b"""
[project]
name = "my_cli_tool"
version = "0.1.0"
"""

# Sample invalid pyproject.toml content
invalid_toml_content = b"""
[project]
name = "my_cli_tool"
version = "0.1.0
"""  # missing closing quote

# Sample toml with missing project section
missing_keys_toml_content = b"""
[other_section]
description = "This is another section"
"""


def test_file_not_found():
    """Test if FileNotFoundError is raised when pyproject.toml doesn't exist."""
    with pytest.raises(FileNotFoundError):
        get_package_metadata("nonexistent_pyproject.toml")


@patch("builtins.open", new_callable=mock_open, read_data=valid_toml_content)
@patch("os.path.exists", return_value=True)
def test_valid_pyproject(mock_exists, mock_file):
    """Test valid pyproject.toml returns correct package name and version."""
    package_name, package_version = get_package_metadata()
    assert package_name == "my_cli_tool"
    assert package_version == "0.1.0"


@patch(
    "builtins.open", new_callable=mock_open, read_data=missing_keys_toml_content
)
@patch("os.path.exists", return_value=True)
def test_missing_keys(mock_exists, mock_file):
    """Test pyproject.toml with missing keys returns defaults."""
    package_name, package_version = get_package_metadata()
    assert package_name == "unknown-package"
    assert package_version == "0.0.0"


@patch("builtins.open", new_callable=mock_open, read_data=invalid_toml_content)
@patch("os.path.exists", return_value=True)
def test_invalid_toml(mock_exists, mock_file):
    """Test invalid TOML raises a RuntimeError."""
    with pytest.raises(RuntimeError):
        get_package_metadata()


@patch("builtins.open", new_callable=mock_open, read_data=valid_toml_content)
@patch("os.path.exists", return_value=True)
def test_get_package_name(mock_exists, mock_file):
    """Test get_package_name returns correct name."""
    assert get_package_name() == "my_cli_tool"


@patch("builtins.open", new_callable=mock_open, read_data=valid_toml_content)
@patch("os.path.exists", return_value=True)
def test_get_package_version(mock_exists, mock_file):
    """Test get_package_version returns correct version."""
    assert get_package_version() == "0.1.0"
