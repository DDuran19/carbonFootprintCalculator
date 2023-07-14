import os, shutil, subprocess, sys

customtkinter_path = sys.executable.replace('python.exe', 'Lib/site-packages/customtkinter')

script_dir = os.path.dirname(os.path.abspath(__file__))
assets_path = os.path.join(script_dir, 'assets')
data_path = os.path.join(script_dir, 'data')
data_json_file = os.path.join(script_dir, 'data.json')
icons_path = os.path.join(script_dir, 'icons')


main_spec = f"""
# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[("{customtkinter_path}", "customtkinter/")],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
    pyinstaller_options=[
        '--noconfirm',
    ],
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main',
)
"""
subprocess.run(["pip", "install", "-r", "requirements.txt"])

with open("main.spec", "w") as file:
    file.write(main_spec)

# Run PyInstaller command with the customtkinter path
subprocess.run(["pyinstaller", "main.spec"])
destination_folder = './dist/main'

# Ensure the destination folder exists
os.makedirs(destination_folder, exist_ok=True)

# Copy the files and directories
shutil.copytree(assets_path, os.path.join(destination_folder, 'assets'))
shutil.copytree(data_path, os.path.join(destination_folder, 'data'))
shutil.copy(data_json_file, os.path.join(destination_folder, 'data.json'))
shutil.copytree(icons_path, os.path.join(destination_folder, 'icons'))
