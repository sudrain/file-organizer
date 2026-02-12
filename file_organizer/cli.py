import typer
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich import print as rprint

from .core import rename_items, delete_files_by_name

# Создаём приложение Typer
app = typer.Typer(
    name="file-organizer",
    help="Утилита для работы с файлами и папками: переименование и удаление.",
    add_completion=False,
)

console = Console()  # одна консоль на всё приложение


@app.command("rename")
def replace_command(
    path: Path = typer.Argument(..., help="Корневая директория", exists=True, file_okay=False, dir_okay=True),
    search: str = typer.Argument(..., help="Подстрока для поиска"),
    replace: str = typer.Argument(..., help="Подстрока для замены"),
    dry_run: bool = typer.Option(False, "--dry-run", "-n", help="Показать что будет изменено без реальных изменений"),
):
    """
    Заменить подстроку в именах файлов и папок (рекурсивно).
    """
    try:
        changes = rename_items(path, search, replace, dry_run=dry_run)
    except Exception as e:
        console.print(f"[red]Ошибка:[/red] {e}")
        raise typer.Exit(code=1)

    if not changes:
        console.print("[yellow]Ничего не найдено для замены.[/yellow]")
        raise typer.Exit()

    # Красивый вывод
    table = Table(title=f"Результаты {'(dry-run)' if dry_run else ''}")
    table.add_column("Было", style="cyan")
    table.add_column("Стало", style="green")
    for old, new in changes:
        table.add_row(str(old), str(new))

    console.print(table)
    console.print(f"[green]Переименовано элементов: {len(changes)}[/green]")


@app.command("remove")
def remove_command(
    path: Path = typer.Argument(..., help="Корневая директория", exists=True, file_okay=False, dir_okay=True),
    name: str = typer.Argument(..., help="Точное имя файла для удаления"),
    dry_run: bool = typer.Option(False, "--dry-run", "-n", help="Показать что будет удалено"),
):
    """
    Удалить все файлы с указанным именем (рекурсивно, только файлы).
    """
    try:
        deleted = delete_files_by_name(path, name, dry_run=dry_run)
    except Exception as e:
        console.print(f"[red]Ошибка:[/red] {e}")
        raise typer.Exit(code=1)

    if not deleted:
        console.print("[yellow]Файлы с таким именем не найдены.[/yellow]")
        raise typer.Exit()

    console.print("[red]Будут удалены:[/red]" if dry_run else "[red]Удалены:[/red]")
    for p in deleted:
        console.print(f"  {p}")
    console.print(f"[green]Всего: {len(deleted)}[/green]")