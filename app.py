from flask import (
    Flask,
    send_file,
    request,
    render_template,
    abort,
    redirect,
    url_for,
    jsonify,
)
import os
import mimetypes
from pathlib import Path
from typing import Optional
from utils import FileIndexer
from dotenv import load_dotenv

app = Flask(__name__)
# read env file!
load_dotenv()

SERVER_DIR = os.getenv("SERVER_DIR", os.getcwd())
indexer = FileIndexer(SERVER_DIR)


def get_file_info(filepath: Path, base_dir: Path) -> dict:
    """Returns a dictionary with file information."""
    is_dir = filepath.is_dir()
    return {
        "name": filepath.name,
        "type": "folder" if is_dir else "file",
        "extension": "" if is_dir else filepath.suffix.lower(),
        "path": str(filepath.relative_to(base_dir)),
        "short_code": indexer.get_short_code(filepath),
    }


def get_sorted_files(current_dir: Optional[Path] = None) -> list:
    """Sorts files and directories, returns detailed information."""
    if current_dir is None:
        current_dir = Path(SERVER_DIR)

    # Remove entries for non-existent files
    indexer.remove_nonexistent()

    # Get and sort items
    items = list(current_dir.iterdir())

    # Separate and sort directories and files
    dirs = sorted([p for p in items if p.is_dir()], key=lambda p: p.name.lower())

    file_types = {
        ".mp4": 1,
        ".avi": 1,
        ".mkv": 1,
        ".webm": 1,  # Videos
        ".jpg": 2,
        ".png": 2,
        ".jpeg": 2,
        ".gif": 2,  # Images
        ".mp3": 3,
        ".wav": 3,
        ".flac": 3,  # Audio
        ".pdf": 4,
        ".txt": 4,
        ".docx": 4,  # Documents
        "other": 6,  # Everything else
    }

    def file_sort_key(filepath):
        return (
            file_types.get(filepath.suffix.lower(), file_types["other"]),
            filepath.name.lower(),
        )

    files = sorted([p for p in items if p.is_file()], key=file_sort_key)

    # Generate file info for all items
    return [get_file_info(p, current_dir) for p in dirs + files]


@app.route("/")
@app.route("/<path:subpath>")
def index(subpath=None):
    """Displays sorted files in a grid UI for the current directory."""
    current_dir = Path(SERVER_DIR) / subpath if subpath else Path(SERVER_DIR)

    if not current_dir.exists() or not current_dir.is_dir():
        abort(404)

    items = get_sorted_files(current_dir)
    return render_template(
        "index.html",
        items=items,
        current_path=subpath or "",
    )


@app.route("/s/<short_code>")
def redirect_to_file(short_code):
    """Redirects short URL to full file/directory URL."""
    rel_path = indexer.get_path(short_code)

    if not rel_path:
        abort(404)

    file_path = Path(SERVER_DIR) / rel_path

    if not file_path.exists():
        abort(404)

    if file_path.is_dir():
        # For directories, redirect to the index view
        rel_path = str(file_path.relative_to(SERVER_DIR))
        return redirect(url_for("index", subpath=rel_path))

    # For files, stream the content
    mime_type = mimetypes.guess_type(str(file_path))[0] or "application/octet-stream"
    return send_file(str(file_path), mimetype=mime_type)


@app.route("/file/<path:filename>")
def stream_file(filename):
    """Streams file efficiently using Range headers."""
    file_path = Path(SERVER_DIR) / filename

    if not file_path.exists() or file_path.is_dir():
        abort(404)

    mime_type = mimetypes.guess_type(str(file_path))[0] or "application/octet-stream"
    return send_file(str(file_path), mimetype=mime_type)


if __name__ == "__main__":
    app.run(
        host=os.getenv("ADDRESS", "0.0.0.0"),
        port=os.getenv("PORT", 5000),
        threaded=True,
        debug=True,
    )
