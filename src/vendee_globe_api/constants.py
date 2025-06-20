from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent.parent

db_path = root_dir / "data" / "vendee_globe.sqlite"
