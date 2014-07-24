"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

import os
from sys import platform

NAME = "Detection"
VERSION = "0.1"
MAIN = "detection.py"
ICON = "icon.icns"

PWD = os.path.dirname(os.path.realpath(__file__))

if platform == "darwin":
    from setuptools import setup
    extra_options = dict(
        setup_requires=['py2app'],
        app=[MAIN],
        options=dict(
            py2app=dict(
                argv_emulation=True,
                iconfile=ICON,
                includes=['PyQt5', 'PyQt5.QtCore',
                          'PyQt5.QtGui', 'PyQt5.QtWidgets'],
                resources=['haarcascades'],
                plist=dict(
                    CFBundleName=NAME,
                    CFBundleShortVersionString=VERSION,
                    CFBundleIconFile=ICON
                    )
                )
            )
        )

def delete_old_app():
    import shutil
    BUILD_PATH = os.path.join(PWD, "build")
    DIST_PATH = os.path.join(PWD, "dist")
    if os.path.exists(BUILD_PATH):
        shutil.rmtree(BUILD_PATH)
    if os.path.exists(DIST_PATH):
        shutil.rmtree(DIST_PATH)

if __name__ == "__main__":
    delete_old_app()
    setup(
        name=NAME,
        version=VERSION,
        author="Yann KOETH",
        data_files=[ICON],
        **extra_options
        )
    if platform == "darwin":
        from os import chmod, makedirs
        from shutil import copyfile
        makedirs('dist/' + NAME + '.app/Contents/PlugIns/platforms')
        copyfile('other/libqcocoa.dylib', 'dist/' + NAME + '.app/Contents/PlugIns/platforms/libqcocoa.dylib')
