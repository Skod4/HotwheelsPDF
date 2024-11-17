import json
import os
from pathlib import Path

class Settings:
    def __init__(self):
        self.settings_file = Path.home() / '.lightpdf_settings.json'
        self.settings = self.load_settings()

    def load_settings(self):
        if self.settings_file.exists():
            try:
                with open(self.settings_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return self.get_default_settings()
        return self.get_default_settings()

    def get_default_settings(self):
        return {
            'preview_enabled': False,
            'default_output_dir': str(Path.home() / 'Documents'),
            'last_used_dir': str(Path.home())
        }

    def save_settings(self):
        with open(self.settings_file, 'w') as f:
            json.dump(self.settings, f)

    def get_preview_enabled(self):
        return self.settings.get('preview_enabled', False)

    def set_preview_enabled(self, enabled):
        self.settings['preview_enabled'] = enabled
        self.save_settings()

    def get_default_output_dir(self):
        return self.settings.get('default_output_dir')

    def set_default_output_dir(self, directory):
        self.settings['default_output_dir'] = directory
        self.save_settings()

    def get_last_used_dir(self):
        return self.settings.get('last_used_dir')

    def set_last_used_dir(self, directory):
        self.settings['last_used_dir'] = directory
        self.save_settings()
