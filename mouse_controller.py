import sys
import json
from PyQt6.QtCore import QSize, Qt, QEvent, QTimer
from PyQt6.QtGui import QAction, QIcon, QKeySequence, QFont
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QSlider, QLabel, QPushButton, QComboBox, QFrame,
    QHBoxLayout, QGroupBox, QTextEdit, QLineEdit,
    QDialog, QDialogButtonBox, QStatusBar, QCheckBox,
    QSpinBox, QTabWidget, QScrollArea, QMessageBox
)

class MacroRecorderDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Macro Recorder")
        self.setModal(True)
        self.resize(400, 300)
        
        layout = QVBoxLayout(self)
        
        # Instructions
        instructions = QLabel("Click 'Start Recording' and then perform the key sequence you want to record.")
        instructions.setWordWrap(True)
        layout.addWidget(instructions)
        
        # Macro display
        self.macro_display = QTextEdit()
        self.macro_display.setReadOnly(True)
        self.macro_display.setMaximumHeight(100)
        layout.addWidget(self.macro_display)
        
        # Control buttons
        control_layout = QHBoxLayout()
        self.record_btn = QPushButton("Start Recording")
        self.record_btn.clicked.connect(self.toggle_recording)
        self.clear_btn = QPushButton("Clear")
        self.clear_btn.clicked.connect(self.clear_macro)
        
        control_layout.addWidget(self.record_btn)
        control_layout.addWidget(self.clear_btn)
        layout.addLayout(control_layout)
        
        # Dialog buttons
        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | 
                                          QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)
        
        # Macro data
        self.macro_keys = []
        self.recording = False
        
    def toggle_recording(self):
        if not self.recording:
            self.recording = True
            self.record_btn.setText("Stop Recording")
            self.macro_keys.clear()
            self.macro_display.clear()
            self.installEventFilter(self)
        else:
            self.recording = False
            self.record_btn.setText("Start Recording")
            self.removeEventFilter(self)
    
    def clear_macro(self):
        self.macro_keys.clear()
        self.macro_display.clear()
    
    def eventFilter(self, obj, event):
        if self.recording and event.type() == QEvent.Type.KeyPress:
            key_name = QKeySequence(event.key()).toString()
            if key_name and key_name not in self.macro_keys:
                self.macro_keys.append(key_name)
                self.macro_display.append(f"Key: {key_name}")
            return True
        return super().eventFilter(obj, event)
    
    def get_macro(self):
        return " + ".join(self.macro_keys)

class ButtonConfigWidget(QWidget):
    def __init__(self, button_number, parent=None):
        super().__init__(parent)
        self.button_number = button_number
        self.parent_controller = parent
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Button label
        self.button_label = QLabel(f"Button {button_number + 1}:")
        self.button_label.setMinimumWidth(80)
        layout.addWidget(self.button_label)
        
        # Function type selector
        self.function_combo = QComboBox()
        self.function_combo.addItems([
            "Left Click", "Right Click", "Middle Click",
            "Scroll Up", "Scroll Down", "DPI Up", "DPI Down",
            "Keystroke", "Macro", "Application", "Disabled"
        ])
        self.function_combo.currentTextChanged.connect(self.update_function)
        layout.addWidget(self.function_combo)
        
        # Parameter input
        self.parameter_input = QLineEdit()
        self.parameter_input.setPlaceholderText("Enter parameter...")
        self.parameter_input.textChanged.connect(self.update_parameter)
        layout.addWidget(self.parameter_input)
        
        # Macro record button
        self.macro_btn = QPushButton("Record Macro")
        self.macro_btn.clicked.connect(self.record_macro)
        self.macro_btn.setVisible(False)
        layout.addWidget(self.macro_btn)
        
        # Store configuration
        self.config = {
            'function': 'Left Click',
            'parameter': ''
        }
    
    def update_function(self, function):
        self.config['function'] = function
        
        # Show/hide parameter input based on function
        if function in ['Keystroke', 'Application']:
            self.parameter_input.setVisible(True)
            self.macro_btn.setVisible(False)
            if function == 'Keystroke':
                self.parameter_input.setPlaceholderText("Enter key combination (e.g., Ctrl+C)")
            else:
                self.parameter_input.setPlaceholderText("Enter application path")
        elif function == 'Macro':
            self.parameter_input.setVisible(True)
            self.macro_btn.setVisible(True)
            self.parameter_input.setPlaceholderText("Macro sequence")
        else:
            self.parameter_input.setVisible(False)
            self.macro_btn.setVisible(False)
    
    def update_parameter(self, text):
        self.config['parameter'] = text
    
    def record_macro(self):
        dialog = MacroRecorderDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            macro = dialog.get_macro()
            self.parameter_input.setText(macro)
            self.config['parameter'] = macro
    
    def get_config(self):
        return self.config.copy()
    
    def set_config(self, config):
        self.config = config
        self.function_combo.setCurrentText(config.get('function', 'Left Click'))
        self.parameter_input.setText(config.get('parameter', ''))

class ProfileManager(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_controller = parent
        
        layout = QVBoxLayout(self)
        
        # Profile selection
        profile_layout = QHBoxLayout()
        profile_layout.addWidget(QLabel("Profile:"))
        
        self.profile_combo = QComboBox()
        self.profile_combo.addItems(["Default", "Gaming", "Office", "Custom 1", "Custom 2"])
        self.profile_combo.currentTextChanged.connect(self.load_profile)
        profile_layout.addWidget(self.profile_combo)
        
        save_btn = QPushButton("Save Profile")
        save_btn.clicked.connect(self.save_profile)
        profile_layout.addWidget(save_btn)
        
        load_btn = QPushButton("Load Profile")
        load_btn.clicked.connect(self.load_profile_file)
        profile_layout.addWidget(load_btn)
        
        layout.addLayout(profile_layout)
        
        # Profile description
        self.profile_desc = QTextEdit()
        self.profile_desc.setMaximumHeight(80)
        self.profile_desc.setPlaceholderText("Profile description...")
        layout.addWidget(self.profile_desc)
    
    def save_profile(self):
        try:
            profile_name = self.profile_combo.currentText()
            profile_data = {
                'name': profile_name,
                'description': self.profile_desc.toPlainText(),
                'dpi': self.parent_controller.dpi_slider.value(),
                'polling_rate': self.parent_controller.polling_rate_combo.currentText(),
                'buttons': {}
            }
            
            # Save button configurations
            for i, button_widget in enumerate(self.parent_controller.button_widgets):
                profile_data['buttons'][i] = button_widget.get_config()
            
            # Save to file
            filename = f"profile_{profile_name.lower().replace(' ', '_')}.json"
            with open(filename, 'w') as f:
                json.dump(profile_data, f, indent=2)
            
            self.parent_controller.statusBar().showMessage(f"Profile '{profile_name}' saved successfully", 3000)
            
        except Exception as e:
            QMessageBox.warning(self, "Save Error", f"Failed to save profile: {str(e)}")
    
    def load_profile_file(self):
        try:
            profile_name = self.profile_combo.currentText()
            filename = f"profile_{profile_name.lower().replace(' ', '_')}.json"
            
            with open(filename, 'r') as f:
                profile_data = json.load(f)
            
            # Load profile data
            self.profile_desc.setPlainText(profile_data.get('description', ''))
            self.parent_controller.dpi_slider.setValue(profile_data.get('dpi', 800))
            self.parent_controller.polling_rate_combo.setCurrentText(profile_data.get('polling_rate', '1000Hz'))
            
            # Load button configurations
            buttons_config = profile_data.get('buttons', {})
            for i, button_widget in enumerate(self.parent_controller.button_widgets):
                if str(i) in buttons_config:
                    button_widget.set_config(buttons_config[str(i)])
            
            self.parent_controller.statusBar().showMessage(f"Profile '{profile_name}' loaded successfully", 3000)
            
        except FileNotFoundError:
            self.parent_controller.statusBar().showMessage(f"Profile file not found", 3000)
        except Exception as e:
            QMessageBox.warning(self, "Load Error", f"Failed to load profile: {str(e)}")
    
    def load_profile(self, profile_name):
        # Auto-load profile when selection changes
        self.load_profile_file()

class MouseController(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Initialize button widgets list first
        self.button_widgets = []
        
        self.setWindowTitle("ROG SPATHA X Controller")
        self.setGeometry(100, 100, 800, 600)
        
        # Set application icon and style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #555555;
                border-radius: 5px;
                margin: 10px;
                padding-top: 10px;
                background-color: #3b3b3b;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #ff6600;
            }
            QPushButton {
                background-color: #ff6600;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #ff8833;
            }
            QPushButton:pressed {
                background-color: #cc5500;
            }
            QSlider::groove:horizontal {
                border: 1px solid #555555;
                height: 8px;
                background: #333333;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #ff6600;
                border: 1px solid #ff6600;
                width: 18px;
                margin: -5px 0;
                border-radius: 9px;
            }
        """)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)
        
        # Main controls tab
        main_tab = QWidget()
        self.setup_main_tab(main_tab)
        self.tab_widget.addTab(main_tab, "Mouse Settings")
        
        # Profile manager tab
        self.profile_manager = ProfileManager(self)
        self.tab_widget.addTab(self.profile_manager, "Profiles")
        
        # Status Bar
        self.setStatusBar(QStatusBar(self))
        self.statusBar().showMessage("ROG SPATHA Controller Ready", 5000)
    
    def setup_main_tab(self, tab_widget):
        layout = QVBoxLayout(tab_widget)
        
        # Create scroll area for button configurations
        scroll = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        
        # DPI Settings
        self.setup_dpi_controls(scroll_layout)
        
        # Polling Rate Settings
        self.setup_polling_rate(scroll_layout)
        
        # Button Functions
        self.setup_button_functions(scroll_layout)
        
        # Advanced Settings
        self.setup_advanced_settings(scroll_layout)
        
        scroll.setWidget(scroll_widget)
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)
    
    def setup_dpi_controls(self, layout):
        dpi_group = QGroupBox("DPI Settings")
        dpi_layout = QVBoxLayout(dpi_group)
        
        # DPI Slider
        slider_layout = QHBoxLayout()
        slider_layout.addWidget(QLabel("400"))
        
        self.dpi_slider = QSlider(Qt.Orientation.Horizontal)
        self.dpi_slider.setRange(400, 19000)
        self.dpi_slider.setValue(800)
        self.dpi_slider.valueChanged.connect(self.update_dpi)
        slider_layout.addWidget(self.dpi_slider)
        
        slider_layout.addWidget(QLabel("19000"))
        dpi_layout.addLayout(slider_layout)
        
        self.dpi_label = QLabel("DPI: 800")
        self.dpi_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.dpi_label.setFont(font)
        dpi_layout.addWidget(self.dpi_label)
        
        # DPI Stages
        stages_layout = QHBoxLayout()
        stages_layout.addWidget(QLabel("DPI Stages:"))
        self.dpi_stages = QSpinBox()
        self.dpi_stages.setRange(1, 5)
        self.dpi_stages.setValue(4)
        stages_layout.addWidget(self.dpi_stages)
        stages_layout.addStretch()
        dpi_layout.addLayout(stages_layout)
        
        layout.addWidget(dpi_group)
    
    def setup_polling_rate(self, layout):
        polling_group = QGroupBox("Polling Rate")
        polling_layout = QVBoxLayout(polling_group)
        
        self.polling_rate_combo = QComboBox()
        self.polling_rate_combo.addItems(["125Hz", "250Hz", "500Hz", "1000Hz"])
        self.polling_rate_combo.setCurrentText("1000Hz")
        self.polling_rate_combo.currentTextChanged.connect(self.update_polling_rate)
        
        polling_layout.addWidget(self.polling_rate_combo)
        layout.addWidget(polling_group)
    
    def setup_button_functions(self, layout):
        button_group = QGroupBox("Button Functions")
        button_layout = QVBoxLayout(button_group)
        
        # Add buttons for each programmable button
        for i in range(12):  # ROG SPATHA has 12 programmable buttons
            button_widget = ButtonConfigWidget(i, self)
            self.button_widgets.append(button_widget)
            button_layout.addWidget(button_widget)
        
        layout.addWidget(button_group)
    
    def setup_advanced_settings(self, layout):
        advanced_group = QGroupBox("Advanced Settings")
        advanced_layout = QVBoxLayout(advanced_group)
        
        # Angle snapping
        self.angle_snapping = QCheckBox("Angle Snapping")
        advanced_layout.addWidget(self.angle_snapping)
        
        # Surface calibration
        surface_layout = QHBoxLayout()
        surface_layout.addWidget(QLabel("Surface Calibration:"))
        self.surface_combo = QComboBox()
        self.surface_combo.addItems(["Auto", "Cloth", "Hard", "Glass", "Custom"])
        surface_layout.addWidget(self.surface_combo)
        surface_layout.addStretch()
        advanced_layout.addLayout(surface_layout)
        
        # Apply settings button
        apply_btn = QPushButton("Apply All Settings")
        apply_btn.clicked.connect(self.apply_all_settings)
        advanced_layout.addWidget(apply_btn)
        
        layout.addWidget(advanced_group)
    
    def update_dpi(self, value):
        self.dpi_label.setText(f"DPI: {value}")
        self.statusBar().showMessage(f"DPI set to {value}", 2000)
        # Here you would add actual mouse DPI setting code
        print(f"Setting DPI to {value}")
    
    def update_polling_rate(self, value):
        self.statusBar().showMessage(f"Polling rate set to {value}", 2000)
        # Here you would add actual polling rate setting code
        print(f"Setting polling rate to {value}")
    
    def apply_all_settings(self):
        # Apply all current settings
        dpi = self.dpi_slider.value()
        polling_rate = self.polling_rate_combo.currentText()
        
        settings_summary = f"Applied: DPI={dpi}, Polling Rate={polling_rate}"
        
        # Count configured buttons
        configured_buttons = sum(1 for widget in self.button_widgets 
                               if widget.config['function'] != 'Left Click' or widget.config['parameter'])
        
        if configured_buttons > 0:
            settings_summary += f", {configured_buttons} buttons configured"
        
        self.statusBar().showMessage(settings_summary, 5000)
        
        # Show confirmation dialog
        QMessageBox.information(self, "Settings Applied", 
                              f"All settings have been applied successfully!\n\n{settings_summary}")

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("ROG SPATHA X Controller")
    app.setApplicationVersion("2.0")
    
    # Set application style
    app.setStyle('Fusion')
    
    window = MouseController()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
