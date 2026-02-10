from pathlib import Path
from typing import List, Tuple


def scan_directory(directory: Path) -> List:
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

    return result


def rename_files(directory: Path, search: str, replace: str) -> List[Tuple[Path, Path]]:
    """
    Рекурсивно переименовывает файлы, заменяя search на replace в именах.
    
    Args:
        directory: Корневая директория
        search: Подстрока для поиска
        replace: Подстрока для замены
    
    Returns:
        Список кортежей (старый_путь, новый_путь)
    """
    if len(search) < 1:
        return []
    
    paths_list = scan_directory(directory)
    new_paths_list = []
    for i in paths_list:
        if search in str(i):
            new_paths_list.append(i.rename(str(i).replace(search, replace)))
        else:
            new_paths_list.append(i)

    if paths_list == new_paths_list:
        return []
    return [tuple(paths_list), (new_paths_list)]

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


