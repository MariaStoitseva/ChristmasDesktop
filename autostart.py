import sys
import winreg
import subprocess

from pathlib import Path


APP_NAME = "ChristmasDesktop"

REGISTRY_PATH = (
    r"Software\Microsoft\Windows\CurrentVersion\Run"
)


def get_startup_command():

    if getattr(sys, "frozen", False):

        # Когато приложението е EXE

        return subprocess.list2cmdline([
            sys.executable
        ])

    # Когато приложението е Python проект

    python_path = Path(sys.executable)

    pythonw_path = python_path.with_name(
        "pythonw.exe"
    )

    if pythonw_path.exists():

        python_path = pythonw_path

    main_path = (
        Path(__file__).resolve().parent
        / "main.py"
    )

    return subprocess.list2cmdline([
        str(python_path),
        str(main_path)
    ])


def is_autostart_enabled():

    try:

        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            REGISTRY_PATH
        ) as key:

            command, _ = winreg.QueryValueEx(
                key,
                APP_NAME
            )

            return command == get_startup_command()

    except FileNotFoundError:

        return False


def set_autostart(enabled):

    if enabled:

        command = get_startup_command()

        if len(command) > 260:

            raise ValueError(
                "Пътят до приложението е твърде дълъг."
            )

        with winreg.CreateKeyEx(
            winreg.HKEY_CURRENT_USER,
            REGISTRY_PATH,
            0,
            winreg.KEY_SET_VALUE
        ) as key:

            winreg.SetValueEx(
                key,
                APP_NAME,
                0,
                winreg.REG_SZ,
                command
            )

    else:

        try:

            with winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                REGISTRY_PATH,
                0,
                winreg.KEY_SET_VALUE
            ) as key:

                winreg.DeleteValue(
                    key,
                    APP_NAME
                )

        except FileNotFoundError:

            pass