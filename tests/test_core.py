from pathlib import Path
import pytest
from file_organizer.core import scan_directory, rename_items


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
        sample_file_structure / "backup" / "nested",
        sample_file_structure / "backup" / "nested" / "nested_file.txt",
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


def test_rename_items_basic(sample_file_structure: Path):
    """Тест: базовое переименование файлов."""
    result = rename_items(sample_file_structure, "file", "document")
    old_path = sample_file_structure / "file1.txt"
    new_path = sample_file_structure / "document1.txt"
    # Возвращает список
    assert isinstance(result, list)
    assert len(result) == 3
    # Проверяем, что файлы переименованы
    assert not old_path.exists()
    assert new_path.exists()
    # Файл без подстроки "file" не должен измениться
    assert (sample_file_structure / "docs" / "doc1.txt").exists()


def test_rename_items_dry_run(sample_file_structure: Path):
    """Тест: проверка какие файлы переименуются."""
    result = rename_items(sample_file_structure, "file", "document", dry_run=True)
    old_path = sample_file_structure / "file1.txt"
    new_path = sample_file_structure / "document1.txt"
    # Возвращает список
    assert isinstance(result, list)
    assert len(result) == 3
    # Проверяем, что файлы переименованы
    assert old_path.exists()
    assert not new_path.exists()


def test_rename_items_no_matches(sample_file_structure: Path):
    """Тест: переименование когда нет совпадений."""
    result = rename_items(sample_file_structure, "xyz", "abc")
    assert result == []  # Ничего не должно измениться
    # Проверяем, что все файлы на месте
    assert (sample_file_structure / "file1.txt").exists()
    assert (sample_file_structure / "docs" / "doc1.txt").exists()


def test_rename_items_empty_string(sample_file_structure: Path):
    """Тест: обработка пустых строк."""
    # result = rename_items(sample_file_structure, "", 'asd' )
    # assert result == [] # сейчас возврат пустого списка, без выполнения логики
    with pytest.raises(ValueError):
        rename_items(sample_file_structure, '', 'asdf')


def test_rename_items_duplicate(sample_file_structure: Path):
    """Тест: обработка если имя занято"""
    directory_ex = sample_file_structure / "directory"
    directory_ex.mkdir()
    result = rename_items(sample_file_structure, "docs", "directory")
    assert result == []
    
