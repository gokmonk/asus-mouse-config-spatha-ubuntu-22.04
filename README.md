# ROG SPATHA X Controller

A comprehensive PyQt6-based GUI application for configuring and managing the ASUS ROG SPATHA gaming mouse. This modern interface provides complete control over all mouse settings, including DPI configuration, polling rates, button mapping, macro recording, and profile management.

![ROG SPATHA Controller](https://img.shields.io/badge/Platform-Linux%20|%20Windows%20|%20macOS-blue)
![Python](https://img.shields.io/badge/Python-3.8+-green)
![PyQt6](https://img.shields.io/badge/PyQt6-GUI-orange)

![Image Description](https://github.com/gokmonk/asus-mouse-config-spatha-ubuntu-22.04/blob/70d9f76ea9cb5ce7e2979e6a6dd40facced7b966/Screenshot%20from%202025-06-10%2023-34-58.png)


## Features

### 🎯 **Mouse Configuration**
- **DPI Control**: Adjustable DPI from 400 to 19,000 with real-time slider
- **Polling Rate**: Configurable polling rates (125Hz, 250Hz, 500Hz, 1000Hz)
- **DPI Stages**: Multiple DPI levels for quick switching during gameplay
- **Surface Calibration**: Optimize tracking for different mouse pad surfaces

### 🔘 **Button Mapping**
- **12 Programmable Buttons**: Full configuration for all ROG SPATHA buttons
- **Multiple Function Types**:
  - Standard mouse functions (Left/Right/Middle click, Scroll)
  - DPI adjustment controls
  - Custom keystroke combinations
  - Recorded macro sequences
  - Application launching
  - Button disable option

### ⚡ **Macro System**
- **Built-in Macro Recorder**: Record complex key sequences with ease
- **Real-time Recording**: Visual feedback during macro creation
- **Flexible Assignment**: Assign macros to any programmable button

### 💾 **Profile Management**
- **Multiple Profiles**: Default, Gaming, Office, and Custom profiles
- **Profile Persistence**: Save/load configurations as JSON files
- **Profile Descriptions**: Add notes and descriptions to each profile
- **Quick Switching**: Instantly switch between different mouse setups

### 🎨 **Modern Interface**
- **Dark Theme**: Professional gaming-oriented design
- **ROG Branding**: Orange accent colors matching ASUS ROG aesthetic
- **Tabbed Interface**: Organized layout for easy navigation
- **Responsive Design**: Scrollable interface handles all configuration options
- **Real-time Feedback**: Status bar updates for all actions

## Installation

### Prerequisites

- Python 3.8 or higher
- PyQt6

### Step 1: Clone or Download

```bash
# Clone the repository (if using git)
git clone <repository-url>
cd rog-spatha-controller

# Or download the single Python file directly
wget <file-url>/mouse_controller.py
```

### Step 2: Install Dependencies

```bash
# Using pip
pip install PyQt6

# Using conda
conda install pyqt

# On Ubuntu/Debian systems, you might also need:
sudo apt-get install python3-pyqt6
```

### Step 3: Run the Application

```bash
python mouse_controller.py
```

## Usage Guide

### Basic Setup

1. **Launch the Application**: Run the Python script to open the controller interface
2. **Configure DPI**: Use the slider to set your preferred sensitivity (400-19,000 DPI)
3. **Set Polling Rate**: Choose your desired polling rate from the dropdown menu
4. **Map Buttons**: Configure each of the 12 programmable buttons according to your needs

### Button Configuration

Each button can be configured with different functions:

- **Standard Functions**: Left Click, Right Click, Middle Click, Scroll Up/Down, DPI Up/Down
- **Keystroke**: Enter custom key combinations (e.g., `Ctrl+C`, `Alt+Tab`, `F1`)
- **Macro**: Record complex key sequences using the built-in macro recorder
- **Application**: Launch specific applications or scripts
- **Disabled**: Completely disable the button

### Creating Macros

1. Select "Macro" from the function dropdown for any button
2. Click the "Record Macro" button
3. In the macro recorder dialog, click "Start Recording"
4. Perform the key sequence you want to record
5. Click "Stop Recording" and then "OK" to save

### Profile Management

1. Switch to the "Profiles" tab
2. Select a profile from the dropdown (Default, Gaming, Office, Custom 1, Custom 2)
3. Configure your mouse settings as desired
4. Add a description in the text area
5. Click "Save Profile" to store your configuration
6. Use "Load Profile" to restore saved settings

### Advanced Settings

- **Angle Snapping**: Enable for perfectly straight lines in drawing applications
- **Surface Calibration**: Choose your mouse pad type for optimal tracking
- **Apply All Settings**: Confirm and apply all current configurations

## File Structure

```
rog-spatha-controller/
├── mouse_controller.py          # Main application file
├── README.md                   # This documentation
├── profile_default.json       # Default profile (auto-generated)
├── profile_gaming.json         # Gaming profile (auto-generated)
├── profile_office.json         # Office profile (auto-generated)
├── profile_custom_1.json       # Custom profile 1 (auto-generated)
└── profile_custom_2.json       # Custom profile 2 (auto-generated)
```

## Configuration Files

Profiles are saved as JSON files with the following structure:

```json
{
  "name": "Gaming",
  "description": "High DPI gaming setup with macro buttons",
  "dpi": 12000,
  "polling_rate": "1000Hz",
  "buttons": {
    "0": {
      "function": "Left Click",
      "parameter": ""
    },
    "1": {
      "function": "Macro",
      "parameter": "Ctrl+C + Ctrl+V"
    }
  }
}
```

## Troubleshooting

### Common Issues

**"ModuleNotFoundError: No module named 'PyQt6'"**
- Install PyQt6 using: `pip install PyQt6`

**Application doesn't start**
- Ensure you're using Python 3.8 or higher
- Check that all dependencies are installed correctly

**Profile files not saving/loading**
- Ensure the application has write permissions in its directory
- Check that the JSON files aren't corrupted

**Mouse settings not applying**
- This is a GUI mockup - actual hardware communication requires mouse drivers
- The interface demonstrates the configuration options available

## Hardware Integration

⚠️ **Important Note**: This application provides a complete GUI interface for mouse configuration but does not include actual hardware communication code. To make it functional with real ROG SPATHA hardware, you would need to:

1. Install ASUS ROG software/drivers
2. Integrate with the mouse's API or driver interface
3. Add hardware communication protocols

The current implementation serves as a comprehensive template and mockup for what such software would look like.

## Development

### Code Structure

- **MouseController**: Main application window and controller
- **ButtonConfigWidget**: Individual button configuration interface
- **MacroRecorderDialog**: Macro recording functionality
- **ProfileManager**: Profile save/load management

### Extending the Application

The modular design makes it easy to add new features:

- Add new button functions in `ButtonConfigWidget`
- Extend macro recording capabilities in `MacroRecorderDialog`
- Add new profile types in `ProfileManager`
- Integrate hardware communication protocols

## Acknowledgments

This application interface was designed and developed with assistance from Claude (Anthropic's AI assistant), who helped visualize and implement the comprehensive GUI design, ensuring a professional and user-friendly gaming peripheral control interface.

## License

This project is provided as-is for educational and development purposes. ASUS and ROG SPATHA are trademarks of ASUSTeK Computer Inc.

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

---

**Note**: This is a GUI demonstration/template. For actual hardware control, integration with official ASUS ROG drivers and APIs would be required.
