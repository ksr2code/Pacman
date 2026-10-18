# PyInstaller spec for the Pac-Man Linux executable.
# Build: make pack  (or: uv run pyinstaller pac-man.spec --noconfirm)


a = Analysis(
    ["pac-man.py"],
    # src/ is on the analysis path: game modules use bare imports
    # (import constants, from maze import Maze, ...).
    pathex=["src"],
    binaries=[],
    datas=[
        # Bare-imported modules (font, sprites, sound via pathex) are
        # bundled top-level: __file__ -> _MEIPASS/<mod>.py, so assets
        # must sit at _MEIPASS/assets. src.main keeps its package prefix
        # and resolves the default config under _MEIPASS/src/.
        ("src/assets", "assets"),
        ("src/config.json", "src"),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,  # onefile mode: single self-extracting executable
    name="Pac-Man",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,  # windowed: no terminal, game window only
)
