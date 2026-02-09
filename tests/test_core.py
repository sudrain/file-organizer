from pathlib import Path
from file_organizer.core import scan_directory


def test_scan_directory_returns_list_of_paths(sample_file_structure):
    """Функция должна возвращать список путей."""
    result = scan_directory(sample_file_structure)
    
    assert isinstance(result, list)
    assert len(result) > 0
    assert all(isinstance(item, Path) for item in result)


def test_scan_directory_includes_files(sample_file_structure):
    """Сканирование должно находить файлы."""
    result = scan_directory(sample_file_structure)
    
    # Проверяем, что находит файлы
    file_paths = [p for p in result if p.is_file()]
    assert len(file_paths) == 4  # file1.txt, doc1.txt, old_file.txt


def test_scan_directory_includes_folders(sample_file_structure):
    """Сканирование должно находить папки."""
    result = scan_directory(sample_file_structure)
    
    # Проверяем, что находит папки
    dir_paths = [p for p in result if p.is_dir()]
    assert len(dir_paths) == 3  # docs, backup


def test_scan_directory_empty_dir(temp_dir):
    """Сканирование пустой директории."""
    result = scan_directory(temp_dir)
    assert result == []


def test_scan_directory_recursive(sample_file_structure):
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