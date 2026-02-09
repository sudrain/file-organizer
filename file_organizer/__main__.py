import typer
from rich.console import Console

app = typer.Typer(help="File Organizer - утилита для работы с файлами")
console = Console()

@app.command()
def version():
    # Версия программы
    console.print("[green]File Organizer v0.1.0[/green]")

def main():
    app()


if __name__ == "__main__":
    main()
