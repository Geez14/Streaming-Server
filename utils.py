import hashlib
import json
from pathlib import Path
from typing import Dict, Optional
import os

class FileIndexer:
    def __init__(self, base_dir: str, index_file: str = '.file_index.json'):
        self.base_dir = Path(base_dir)
        self.index_file = Path(os.getenv("SERVER_INDEX", self.base_dir))
        if not self.index_file.exists():
            self.index_file.mkdir(555)
        self.index_file = self.index_file.joinpath(index_file)
        print(self.index_file)
        self.file_map: Dict[str, str] = {}  # short_code -> relative_path
        self.path_map: Dict[str, str] = {}  # relative_path -> short_code
        self.load_index()

    def load_index(self):
        """Load existing index from file if it exists."""
        try:
            if self.index_file.exists():
                with open(self.index_file, 'r') as f:
                    data = json.load(f)
                    self.file_map = data.get('file_map', {})
                    self.path_map = data.get('path_map', {})
        except Exception as e:
            print(f"Error loading index: {e} | or no index exists")
            self.file_map = {}
            self.path_map = {}

    def save_index(self):
        """Save current index to file."""
        try:
            with open(self.index_file, 'w') as f:
                json.dump({
                    'file_map': self.file_map,
                    'path_map': self.path_map
                }, f, indent=2)
        except Exception as e:
            print(f"Error saving index: {e}")

    def generate_short_code(self, path: str) -> str:
        """Generate a unique short code for a path."""
        return hashlib.md5(path.encode()).hexdigest()[:16]

    def get_short_code(self, full_path: Path) -> str:
        """Get or create short code for a path."""
        rel_path = str(full_path.relative_to(self.base_dir))
        
        # Return existing code if path is already indexed
        if rel_path in self.path_map:
            return self.path_map[rel_path]
        
        # Generate new code and ensure it's unique
        while True:
            short_code = self.generate_short_code(rel_path)
            if short_code not in self.file_map:
                self.file_map[short_code] = rel_path
                self.path_map[rel_path] = short_code
                self.save_index()
                return short_code
            # In case of collision, append a counter to the path
            rel_path = f"{rel_path}_{len(self.file_map)}"

    def get_path(self, short_code: str) -> Optional[str]:
        """Get path from short code."""
        return self.file_map.get(short_code)

    def remove_nonexistent(self):
        """Remove entries for files that no longer exist."""
        to_remove_file = []
        to_remove_path = []
        
        for short_code, rel_path in self.file_map.items():
            full_path = self.base_dir / rel_path
            if not full_path.exists():
                to_remove_file.append(short_code)
                to_remove_path.append(rel_path)
        
        for code in to_remove_file:
            del self.file_map[code]
        for path in to_remove_path:
            del self.path_map[path]
        
        if to_remove_file:
            self.save_index()
