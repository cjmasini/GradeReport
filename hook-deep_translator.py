# hook-deep_translator.py
from PyInstaller.utils.hooks import collect_submodules

hiddenimports = collect_submodules('deep_translator')