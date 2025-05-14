"""Module for package versioning."""

import contextlib
import re
from importlib import metadata
from typing import Optional

def get_version() -> str:
    """Retrieves the version of the package from a possible list of package names.

    This accounts for after package names are updated for -nightly builds.

    Returns:
        str: The version of the package

    Raises:
        ValueError: If the package is not found from the list of package names.
    """
    pkg_names = [
        "langflow",
        "langflow-base",
        "langflow-nightly",
        "langflow-base-nightly",
    ]
    version = None
    errors = []
    
    for pkg_name in pkg_names:
        try:
            version = metadata.version(pkg_name)
            break
        except (ImportError, metadata.PackageNotFoundError) as e:
            errors.append(f"{pkg_name}: {str(e)}")

    if version is None:
        msg = f"Package not found from options {pkg_names}. Errors: {'; '.join(errors)}"
        raise ValueError(msg)

    return version

def parse_version(version_str: str) -> tuple[int, int, int, Optional[str]]:
    """Parse version string into its components.
    
    Args:
        version_str (str): Version string in format "X.Y.Z[suffix]"
        
    Returns:
        tuple: (major, minor, patch, suffix)
    """
    pattern = r"(\d+)\.(\d+)\.(\d+)(.*)?"
    match = re.match(pattern, version_str)
    if not match:
        raise ValueError(f"Invalid version format: {version_str}")
    
    major, minor, patch, suffix = match.groups()
    return (int(major), int(minor), int(patch), suffix or None)

def is_pre_release(v: str) -> bool:
    """Returns a boolean indicating whether the version is a pre-release version.

    Returns a boolean indicating whether the version is a pre-release version,
    as per the definition of a pre-release segment from PEP 440.
    """
    return any(label in v for label in ["a", "b", "rc", "dev"])
