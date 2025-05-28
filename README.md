# PyNeko

A Python implementation of the classic Neko (猫, cat) desktop pet, inspired by the original [Neko project](https://github.com/crgimenes/neko).

![PyNeko Demo](assets/photo/awake.png)

## Description

PyNeko is a desktop pet that follows your mouse cursor around the screen. It features multiple animations, sounds, and behaviors just like a real cat!

## Features

- 8-directional smooth movement
- Multiple animation states (sleeping, washing, scratching, yawning)
- Sound effects
- Configurable settings via INI file
- Transparent window that stays on top
- Cross-platform support (Windows, macOS)

## Requirements

- Python 3.7+
- tkinter (usually comes with Python)
- pygame (for sound support)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/pyneko.git
cd pyneko
```

2. Install dependencies:
```bash
pip install pygame
```

## Configuration

Create a `neko.ini` file in the project root directory:

```ini
[DEFAULT]
speed = 2
scale = 2.0
quiet = false
mousepassthrough = false
```

### Configuration Options

- `speed`: Movement speed (default: 2)
- `scale`: Window scale factor (default: 2.0)
- `quiet`: Disable sound effects (default: false)
- `mousepassthrough`: Enable click-through window (default: false)

## Directory Structure

```
pyneko/
├── main.py
├── neko.ini
└── assets/
    ├── photo/
    │   ├── awake.png
    │   ├── sleep.png
    │   ├── up1.png
    │   ├── up2.png
    │   └── ...
    └── sounds/
        ├── idle3.wav
        ├── awake.wav
        └── sleep.wav
```

## Usage

Run the application:
```bash
python main.py
```

### Controls

- Left-click: Toggle between active/waiting state
- The cat will automatically follow your cursor when active

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Original [Neko project](https://github.com/crgimenes/neko) by crgimenes
- Inspired by the classic Neko desktop pet from the 1990s