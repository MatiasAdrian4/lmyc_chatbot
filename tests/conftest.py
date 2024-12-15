import tempfile
from pathlib import Path

import pytest

from database import Database


@pytest.fixture
def setup_database():
    """Fixture to provide a temporary database for testing."""
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        temp_file = Path(tmp.name)
    database = Database(file=temp_file)
    yield database
    temp_file.unlink()  # clean up after tests
