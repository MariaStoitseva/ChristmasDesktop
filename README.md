<div align="center">

<img src="assets/icon.png" width="120" alt="Christmas Desktop Logo">

# Christmas Desktop

### Bring the magic of Christmas to your Windows desktop.

![Version](https://img.shields.io/badge/version-1.0.0-green)
![Python](https://img.shields.io/badge/Python-3.12-blue)
![PySide6](https://img.shields.io/badge/PySide6-Qt-green)
![Platform](https://img.shields.io/badge/platform-Windows-blue)

[Download for Windows](https://github.com/MariaStoitseva/ChristmasDesktop/releases/latest)

</div>

---

## About

Christmas Desktop is an interactive Windows desktop
application that brings a festive winter atmosphere
to your everyday workspace.

It combines animated snowfall, realistic snow
accumulation, dynamic winter wallpapers and interactive
Christmas decorations into a customizable desktop
experience.

The application runs in the background and can be
managed directly from the Windows system tray.

## Features

### Animated Snowfall

- Animated snowflakes across the screen.
- Snow accumulation on window edges.
- Snow accumulation above the taskbar.
- Falling snow when windows are moved or closed.
- Toggle snowfall on or off.

### Dynamic Wallpapers

Four matching winter landscapes that automatically
change throughout the day.

| Time | Wallpaper |
|------|-----------|
| 06:00 - 09:00 | Sunrise |
| 09:00 - 16:00 | Day |
| 16:00 - 18:00 | Sunset |
| 18:00 - 06:00 | Night |

- Automatic wallpaper switching.
- Manual wallpaper selection.
- Restore the original desktop wallpaper.

### Interactive Snowmen

- Create snowmen by stacking three snowballs.
- Drag and move snowballs around the desktop.
- Build up to five snowmen.
- Five different snowman designs.
- Customizable scarf colors and hats.
- Move or remove completed snowmen.

### Christmas Trees

- Add up to three interactive Christmas trees.
- Move trees anywhere on the desktop.
- Customize Christmas ornaments.
- Animated colorful lights.
- Candy canes and garlands.
- Christmas stars.
- Decorative presents.
- Snow accumulation on branches.

### Snowplow

- Animated snowplow traveling across the screen.
- Clears accumulated snow above the taskbar.
- Adjustable automatic interval.
- Manual activation.

### Christmas Train

- Animated festive locomotive.
- Decorated wagons carrying Christmas presents.
- Animated smoke and wheels.
- Adjustable automatic interval.
- Manual activation.

### Settings Panel

- Enable or disable snowfall.
- Select wallpaper mode.
- Customize animation intervals.
- Create snowballs and Christmas trees.
- Manually launch festive animations.
- Enable automatic startup with Windows.

## Screenshots

### Christmas Desktop

![Desktop](screenshots/desktop.png)

### Settings Panel

![Settings](screenshots/settings.png)

### Interactive Decorations

![Decorations](screenshots/decorations.png)

### Dynamic Wallpapers

| Sunrise | Day |
|---------|-----|
| ![Sunrise](assets/winter_sunrise.png) | ![Day](assets/winter_day.png) |

| Sunset | Night |
|--------|-------|
| ![Sunset](assets/winter_sunset.png) | ![Night](assets/winter_night.png) |

## Download and Installation

1. Open the [Releases page](https://github.com/MariaStoitseva/ChristmasDesktop/releases/latest).
2. Download `ChristmasDesktopSetup.exe`.
3. Run the installer.
4. Follow the installation instructions.
5. Launch Christmas Desktop.

No Python installation is required.

The installer is currently unsigned, so Windows
may display a SmartScreen warning.

## How to Use

1. Launch Christmas Desktop.
2. Find the snowflake icon in the Windows system tray.
3. Left-click the icon to open the settings panel.
4. Customize your winter desktop.
5. Right-click the icon and select Exit to close
   the application.

You can move and customize interactive decorations
directly on your desktop.

## System Requirements

- Windows 10 or Windows 11 (64-bit).
- Suitable for standard desktop and laptop computers.

The application was developed and tested on Windows 11.

## Technologies

- Python 3.12
- PySide6
- Qt Widgets
- QPainter
- Windows API
- PyWin32
- Pillow
- PyInstaller
- Inno Setup

## Project Structure

```text
ChristmasDesktop/
│
├── assets/
│   ├── icon.ico
│   ├── icon.png
│   ├── winter_day.png
│   ├── winter_night.png
│   ├── winter_sunrise.png
│   └── winter_sunset.png
│
├── screenshots/
│
├── main.py
├── overlay.py
├── snow.py
├── snowball.py
├── snowman.py
├── snowman_manager.py
├── snowplow.py
├── christmas_tree.py
├── tree_manager.py
├── christmas_train.py
├── window_manager.py
├── wallpaper.py
├── settings_window.py
├── tray.py
├── autostart.py
├── create_icon.py
├── installer.iss
├── requirements.txt
├── .gitignore
└── README.md
```

## Run from Source

Clone the repository:

```bash
git clone https://github.com/MariaStoitseva/ChristmasDesktop.git
cd ChristmasDesktop
```

Create a virtual environment:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Run the application:

```bash
python main.py
```

## Build the Executable

```powershell
python -m PyInstaller --noconfirm --clean --onedir --windowed --name ChristmasDesktop --icon "assets/icon.ico" --add-data "assets:assets" main.py
```

The executable will be available in:

```text
dist/ChristmasDesktop/
```

Keep the executable and its `_internal` directory
together.

## Build the Installer

1. Install Inno Setup.
2. Build the executable using PyInstaller.
3. Open `installer.iss` in Inno Setup.
4. Compile the installer.

The installer will be generated in:

```text
installer/ChristmasDesktopSetup.exe
```

## Author

**Maria Stoitseva**

Python Developer | Software Technologies and Design Student

GitHub: [MariaStoitseva](https://github.com/MariaStoitseva)

---

<div align="center">

Made with Python, creativity and a little Christmas magic.

Merry Christmas!

</div>