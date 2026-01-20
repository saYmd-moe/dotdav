
import yaml
from pathlib import Path

CONFIG_FILE = Path("config.yaml")
MAPPINGS_FILE = Path("mappings.yaml")
REPO_DIR = Path("repo")

class Config:
    def __init__(self):
        self.data = {
            "rclone_remote": "",
            "rclone_path": "dotfiles",
            "current_profile": "default",
            "debounce_seconds": 5,
            "sync_interval_minutes": 10
        }
        self.load()

    def load(self):
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, "r") as f:
                self.data.update(yaml.safe_load(f) or {})

    def save(self):
        with open(CONFIG_FILE, "w") as f:
            yaml.safe_dump(self.data, f)
    
    def get(self, key):
        return self.data.get(key)

    def set(self, key, value):
        self.data[key] = value
        self.save()

class Mappings:
    def __init__(self):
        self.data = {"files": {}}
        self.load()

    def load(self):
        if MAPPINGS_FILE.exists():
            with open(MAPPINGS_FILE, "r") as f:
                self.data.update(yaml.safe_load(f) or {})
        if "files" not in self.data:
            self.data["files"] = {}

    def save(self):
        with open(MAPPINGS_FILE, "w") as f:
            yaml.safe_dump(self.data, f)

    def add_file(self, name, profile, repo_filename):
        if name not in self.data["files"]:
            self.data["files"][name] = {}
        self.data["files"][name][profile] = repo_filename
        self.save()

    def get_repo_file(self, name, profile):
        files = self.data["files"].get(name, {})
        return files.get(profile) or files.get("default")
