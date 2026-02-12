import pytest
from typer.testing import CliRunner
from pathlib import Path
from unittest.mock import patch

from file_organizer.cli import app

runner = CliRunner()


def test_rename_command_basic(temp_dir):
    """Проверяем, что команда rename вызывает core.rename_items с правильными аргументами."""
    with patch("file_organizer.cli.rename_items") as mock_rename:
        mock_rename.return_value = [
            (temp_dir / "old_file.txt", temp_dir / "old_document.txt")
        ]
        result = runner.invoke(
            app, ["rename", str(temp_dir), "file", "document"]
        )
        assert result.exit_code == 0
        mock_rename.assert_called_once_with(
            temp_dir, "file", "document", dry_run=False
        )
        assert "old_file.txt" in result.stdout
        assert "old_document.txt" in result.stdout


def test_rename_command_dry_run(temp_dir):
    """Проверяем флаг --dry-run."""
    with patch("file_organizer.cli.rename_items") as mock_rename:
        mock_rename.return_value = [(temp_dir / "old_file.txt", temp_dir / "old_document.txt")]
        result = runner.invoke(
            app, ["rename", str(temp_dir), "file", "document", "--dry-run"]
        )
        assert result.exit_code == 0
        mock_rename.assert_called_once_with(
            temp_dir, "file", "document", dry_run=True
        )
        assert "(dry-run)" in result.stdout


def test_rename_command_no_matches(temp_dir):
    """Если rename_items вернул пустой список — должно быть сообщение и выход без ошибки."""
    with patch("file_organizer.cli.rename_items") as mock_rename:
        mock_rename.return_value = []
        result = runner.invoke(
            app, ["rename", str(temp_dir), "xyz", "abc"]
        )
        assert result.exit_code == 0
        assert "Ничего не найдено" in result.stdout


def test_rename_command_error(temp_dir):
    """Если rename_items кидает исключение — программа должна завершиться с ошибкой."""
    with patch("file_organizer.cli.rename_items") as mock_rename:
        mock_rename.side_effect = FileNotFoundError("Директория не найдена")
        result = runner.invoke(
            app, ["rename", str(temp_dir), "a", "b"]
        )
        assert result.exit_code == 1
        assert "Директория не найдена" in result.stdout


def test_remove_command_basic(temp_dir):
    """Проверяем команду remove."""
    with patch("file_organizer.cli.delete_files_by_name") as mock_delete:
        mock_delete.return_value = [temp_dir / "file.txt"]
        result = runner.invoke(
            app, ["remove", str(temp_dir), "file.txt"]
        )
        assert result.exit_code == 0
        mock_delete.assert_called_once_with(temp_dir, "file.txt", dry_run=False)
        assert "Удалены" in result.stdout


def test_remove_command_dry_run(temp_dir):
    """remove с --dry-run."""
    with patch("file_organizer.cli.delete_files_by_name") as mock_delete:
        mock_delete.return_value = [temp_dir / "file.txt"]
        result = runner.invoke(
            app, ["remove", str(temp_dir), "file.txt", "--dry-run"]
        )
        assert result.exit_code == 0
        mock_delete.assert_called_once_with(temp_dir, "file.txt", dry_run=True)
        assert "Будут удалены" in result.stdout


def test_path_validation():
    """Typer сам валидирует exists=True, ошибка должна выводиться в stderr."""
    result = runner.invoke(app, ["rename", "/nonexistent/path", "a", "b"])
    assert result.exit_code != 0
    # Typer пишет ошибки в stderr
    assert "does not exist" in result.stderr.lower() or "не существует" in result.stderr