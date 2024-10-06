import os

import tomli


def get_package_metadata(pyproject_path=None):
    """Read the package name and version from pyproject.toml."""
    if pyproject_path is None:
        pyproject_path = default_pyproject_file()
    if not os.path.exists(pyproject_path):
        raise FileNotFoundError(f"{pyproject_path} not found")

    try:
        with open(pyproject_path, "rb") as file:
            pyproject_data = tomli.load(file)
            # Navigate to the relevant section of pyproject.toml
            project_metadata = pyproject_data.get("project", {})
            package_name = project_metadata.get("name", "unknown-package")
            package_version = project_metadata.get("version", "0.0.0")
            return package_name, package_version
    except (KeyError, FileNotFoundError, tomli.TOMLDecodeError) as e:
        raise RuntimeError(f"Error reading pyproject.toml: {e}") from e


def default_pyproject_file():
    return os.path.realpath(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "..",
            "..",
            "pyproject.toml",
        )
    )


def get_package_name():
    """Return the package name from pyproject.toml."""
    package_name, _ = get_package_metadata()
    return package_name


def get_package_version():
    """Return the package version from pyproject.toml."""
    _, package_version = get_package_metadata()
    return package_version


__title__ = get_package_name()
__version__ = get_package_version()

if __name__ == "__main__":
    print(get_package_metadata())
