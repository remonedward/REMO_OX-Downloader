import PyInstaller.__main__
import os

# Define project details
EXE_NAME = "REMO_OX_Downloader"
ICON_FILE = "ox.ico"
MAIN_SCRIPT = "main.py"

# Include bin folder (FFmpeg) as data
# Path structure for PyInstaller: (source_path, target_folder_name_in_bundle)
bin_data = 'bin;bin'

# Run PyInstaller
PyInstaller.__main__.run([
    MAIN_SCRIPT,
    '--onefile',
    '--windowed',
    f'--icon={ICON_FILE}',
    f'--name={EXE_NAME}',
    f'--add-data={bin_data}',
    '--clean',
    '--noconfirm'
])
