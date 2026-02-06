# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['WASAPIRecording.pyw'],
    pathex=[],
    binaries=[],
    datas=[
        ('sound_lib', 'sound_lib'),
        ('locales', 'locales'),
        ('icono.ico', '.'),
    ],
    hiddenimports=['platform_utils', 'libloader'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='WASAPIRecording',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    console=False,  # Sin consola
    icon='icono.ico',  # Ruta del ícono
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
    name='WASAPIRecording',  # Cambiar el nombre de la carpeta a 'lib'
)
