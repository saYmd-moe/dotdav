
import yaml
from pathlib import Path

CONFIG_FILE = Path("config.yaml")
LOCAL_CONFIG_FILE = Path("config.local.yaml")
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
        # Load base config
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, "r") as f:
                self.data.update(yaml.safe_load(f) or {})
        
        # Load local config overrides
        if LOCAL_CONFIG_FILE.exists():
            with open(LOCAL_CONFIG_FILE, "r") as f:
                local_data = yaml.safe_load(f) or {}
                self.data.update(local_data)

    def save(self):
        # Always save changes to local config to avoid polluting shared config
        # We need to read existing local config first to preserve keys we might not track in self.data 
        # (though currently self.data seems to hold everything)
        # Ideally, we only save what is different from defaults or base? 
        # For simple implementation: save all current state to local config.
        # OR: To be cleaner, we might want to only save *changed* values, 
        # but tracking changes is complex. 
        # Let's save the entire current state to local config as it overrides everything anyway.
        
        with open(LOCAL_CONFIG_FILE, "w") as f:
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
