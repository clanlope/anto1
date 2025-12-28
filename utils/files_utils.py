from pathlib import Path
import inspect


def current_dir() -> Path:
    """Returns the directory of the current file."""
    return Path(inspect.stack()[-1].filename).resolve().parent


def ensure_dir(path: Path) -> None:
    """Ensure directory exists. Create it if missing."""
    Path(path).mkdir(parents=True, exist_ok=True)


def list_files(suffix: str = "", directory: Path = None) -> list[Path] | list[None]:
    """Lists all files in the given directory."""
    suffix = suffix.lower() if suffix.startswith(".") else f".{suffix.lower()}"
    directory = current_dir() if directory is None else directory
    return [
        _
        for _ in directory.iterdir()
        if _.is_file() and (suffix == "" or _.suffix == suffix)
    ]


def get_prefix(file: Path) -> str:
    """Gets the prefix of a file (part before '@')."""
    if "@" not in file.stem:
        raise ValueError(f"No '@' in filename: {file.name}")
    return file.stem.split("@", 1)[0]


def match_prefix(file1: Path, file2: Path) -> bool:
    """Checks if two files have the same prefix."""
    return get_prefix(file1) == get_prefix(file2)


def select_file(list: list[Path]) -> Path | None:
    """⚪ Selects a file from the file list: [0 quit]"""
    print(inspect.getdoc(select_file))
    [print(i + 1, v) for i, v in enumerate(list)]
    while True:
        try:
            res = list[u - 1] if (u := int(input())) else None
            print(f"🔵 Your selection: {res.name if res else 'None'}")
            return res
        except Exception as e:
            print(f"❌ Invalid selection, try again. -> {e}")
