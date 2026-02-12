import pytest
import tempfile
from pathlib import Path
import shutil


@pytest.fixture
def temp_dir():
    """Создает временную директорию для тестов."""
    tmpdir = tempfile.mkdtemp()
    yield Path(tmpdir)
    shutil.rmtree(tmpdir)


@pytest.fixture
def sample_file_structure(temp_dir: Path):
    """
    Структура:
    temp_dir/
    ├── file1.txt
    ├── docs/
    │   └── doc1.txt
    ├── file_folder/
    │   └── inner.txt
    └── backup/
        └── old_file.txt
            nested/
            └── nested_file.txt
    """
    # Создаем файлы
    (temp_dir / "file1.txt").write_text("content1")
    
    # Создаем подпапку docs с файлом
    docs_dir = temp_dir / "docs"
    docs_dir.mkdir()
    (docs_dir / "doc1.txt").write_text("document content")
    
    # Создаем подпапку backup с файлом
    backup_dir = temp_dir / "backup"
    backup_dir.mkdir()
    (backup_dir / "old_file.txt").write_text("old content")

    # Создаем подпапку с файлом
    file_dir = temp_dir / "file_folder"
    file_dir.mkdir()
    (file_dir / "inner.txt").write_text("inner content")

    # backup nested
    backup_nested_dir = backup_dir / "nested"
    backup_nested_dir.mkdir()
    (backup_nested_dir / "nested_file.txt").write_text("nested content")
    
    return temp_dir