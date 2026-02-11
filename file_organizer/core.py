from pathlib import Path
from typing import List, Tuple


def scan_directory(directory: Path) -> List[Path]:
    """
    Рекурсивно сканирует директорию и возвращает список всех файлов и папок.
    
    Args:
        directory: Путь к директории для сканирования
    
    Returns:
        Список путей Path ко всем файлам и папкам
    """

    if not directory.exists():
        raise FileNotFoundError(f"Директория не существует: {directory}")
    if not directory.is_dir():
        raise NotADirectoryError(f"Путь не является директорией: {directory}")
    
    result = []
    for path in directory.rglob("*"):
        result.append(path)

    return sorted(result, key=lambda p: len(p.parents), reverse=True)


def rename_items(directory: Path, search: str, replace: str) -> List[Tuple[Path, Path]]:
    """
    Рекурсивно переименовывает файлы и папки, заменяя search на replace в именах.
    
    Args:
        directory: Корневая директория
        search: Подстрока для поиска
        replace: Подстрока для замены
    
    Returns:
        Список кортежей (старый_путь, новый_путь) для успешно переименованных элементов.
    """
    if len(search) < 1 or not isinstance(search, str):
        raise ValueError("Параметр 'search' должен быть строкой с длинной более 0")

    
    paths_list = scan_directory(directory)
    changed_paths = []
    
    for path in paths_list:
        if search not in path.name:
            continue
        
        new_name = path.name.replace(search, replace)
        if new_name == path.name:
            continue
        
        new_path = path.parent / new_name
        if new_path.exists():
            # Лучше заменить print на логирование позже
            print(f"Предупреждение: {new_path} уже существует, пропускаем")
            continue
        
        changed_paths.append((path, path.rename(new_path)))
    
    return changed_paths

def delete_files_by_name(directory: Path, filename: str) -> List[Path]:
    """
    Рекурсивно удаляет файлы с указанным именем.
    
    Args:
        directory: Корневая директория
        filename: Имя файла для удаления
    
    Returns:
        Список путей к удаленным файлам
    """
    # TODO: Реализовать
    raise NotImplementedError("Функция пока не реализована")


