from pathlib import Path
import pytest
from file_organizer.core import scan_directory, rename_files


def test_scan_directory_returns_list_of_paths(sample_file_structure: Path):
    """Функция должна возвращать список путей."""
    result = scan_directory(sample_file_structure)
    
    assert isinstance(result, list)
    assert len(result) > 0
    assert all(isinstance(item, Path) for item in result)


def test_scan_directory_includes_files(sample_file_structure: Path):
    """Сканирование должно находить файлы."""
    result = scan_directory(sample_file_structure)
    
    # Проверяем, что находит файлы
    file_paths = [p for p in result if p.is_file()]
    assert len(file_paths) == 4  # file1.txt, doc1.txt, old_file.txt


def test_scan_directory_includes_folders(sample_file_structure: Path):
    """Сканирование должно находить папки."""
    result = scan_directory(sample_file_structure)
    
    # Проверяем, что находит папки
    dir_paths = [p for p in result if p.is_dir()]
    assert len(dir_paths) == 3  # docs, backup


def test_scan_directory_empty_dir(temp_dir: Path):
    """Сканирование пустой директории."""
    result = scan_directory(temp_dir)
    assert result == []


def test_scan_directory_recursive(sample_file_structure: Path):
    """Рекурсивное сканирование."""
    result = scan_directory(sample_file_structure)

    # Должны найти все 7 элементов (4 файла + 3 папки)
    assert len(result) == 7

    # Проверяем конкретные пути
    expected_paths = [
        sample_file_structure / "file1.txt",
        sample_file_structure / "docs",
        sample_file_structure / "docs" / "doc1.txt",
        sample_file_structure / "backup",
        sample_file_structure / "backup" / "old_file.txt",
        sample_file_structure / "backup" / "backup_nested",
        sample_file_structure / "backup" / "backup_nested" / "nested_file.txt",
    ]
    
    for expected in expected_paths:
        assert expected in result


def test_scan_directory_nonexistent():
    """Тест: обработка несуществующей директории."""
    with pytest.raises(FileNotFoundError):
        scan_directory(Path("/несуществующая/директория"))


def test_scan_directory_not_a_directory(temp_dir: Path):
    """Тест: обработка когда путь - файл, а не директория."""
    # Создаем файл
    file_path = temp_dir / "file.txt"
    file_path.write_text("test")
    
    with pytest.raises(NotADirectoryError):
        scan_directory(file_path)


def test_rename_files_basic(sample_file_structure: Path):
    """Тест: базовое переименование файлов."""
    result = rename_files(sample_file_structure, "file", "document")
    old_path = sample_file_structure / "file1.txt"
    new_path = sample_file_structure / "document1.txt"
    # Возвращает список
    assert isinstance(result, list)
    assert len(result) == 2

    # Проверяем изменения в возвращенном списке
    assert old_path in result[0]
    assert new_path in result[1]

    # Проверяем, что файлы переименованы
    assert not old_path.exists()
    assert new_path.exists()
    assert not (sample_file_structure / "backup" / "old_file.txt").exists()
    assert (sample_file_structure / "backup" / "old_document.txt").exists()