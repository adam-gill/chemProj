import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QFileDialog, QHBoxLayout
from PyQt6.QtGui import QClipboard
from compare import compare_images
from PyQt6.QtCore import QTimer


class SimpleApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.file1_path = ""
        self.file2_path = ""
        
    def initUI(self):
        # Set base sizes
        self.base_width = 800
        self.base_height = 400
        self.font_size = 14
        
        layout = QVBoxLayout()
        
        # Create a style sheet for consistent sizing
        style = f"""
            QPushButton {{
                font-size: {self.font_size}px;
                padding: 10px;
                min-width: 120px;
                min-height: 40px;
            }}
            QLabel {{
                font-size: {self.font_size}px;
            }}
        """
        self.setStyleSheet(style)
        
        # First file selection
        file1_layout = QHBoxLayout()
        self.file1_label = QLabel("No file selected")
        file1_button = QPushButton("Select First File")
        file1_button.clicked.connect(lambda: self.browse_file(1))
        file1_layout.addWidget(file1_button)
        file1_layout.addWidget(self.file1_label)
        
        # Second file selection
        file2_layout = QHBoxLayout()
        self.file2_label = QLabel("No file selected")
        file2_button = QPushButton("Select Second File")
        file2_button.clicked.connect(lambda: self.browse_file(2))
        file2_layout.addWidget(file2_button)
        file2_layout.addWidget(self.file2_label)
        
        # Submit and Reset buttons
        button_layout = QHBoxLayout()
        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(self.check_files)
        reset_button = QPushButton("Reset")
        reset_button.clicked.connect(self.reset_fields)
        
        button_layout.addWidget(submit_button)
        button_layout.addWidget(reset_button)

        # SSIM display with copy button
        self.ssim_label = QLabel("")
        self.ssim_copy_button = QPushButton("Copy SSIM")
        self.ssim_copy_button.clicked.connect(lambda: self.copy_to_clipboard(self.ssim_label.text()))
        self.ssim_copy_button.setVisible(False)  # Initially hidden
        ssim_layout = QHBoxLayout()
        ssim_layout.addWidget(self.ssim_label)
        ssim_layout.addWidget(self.ssim_copy_button)

        # MSE display with copy button
        self.mse_label = QLabel("")
        self.mse_copy_button = QPushButton("Copy MSE")
        self.mse_copy_button.clicked.connect(lambda: self.copy_to_clipboard(self.mse_label.text()))
        self.mse_copy_button.setVisible(False)  # Initially hidden
        mse_layout = QHBoxLayout()
        mse_layout.addWidget(self.mse_label)
        mse_layout.addWidget(self.mse_copy_button)

        layout.addLayout(file1_layout)
        layout.addLayout(file2_layout)
        layout.addLayout(button_layout)
        layout.addLayout(ssim_layout)
        layout.addLayout(mse_layout)
        
        self.setLayout(layout)
        self.setWindowTitle('Image Comparison App')
        self.setGeometry(300, 300, self.base_width, self.base_height)
        
    def browse_file(self, file_num):
        filename, _ = QFileDialog.getOpenFileName(self, 'Select File', '', 'All Files (*)')
        if filename:
            if file_num == 1:
                self.file1_path = filename
                self.file1_label.setText(filename.split('/')[-1])
            else:
                self.file2_path = filename
                self.file2_label.setText(filename.split('/')[-1])

    def reset_fields(self):
        self.file1_path = ""
        self.file2_path = ""
        self.file1_label.setText("No file selected")
        self.file2_label.setText("No file selected")
        self.ssim_label.setText("")
        self.mse_label.setText("")
        # Reset copy button states
        self.ssim_copy_button.setText("Copy SSIM")
        self.mse_copy_button.setText("Copy MSE")
        self.ssim_copy_button.setVisible(False)
        self.mse_copy_button.setVisible(False)
        # Reset label styles
        self.ssim_label.setStyleSheet("")
        self.mse_label.setStyleSheet("")

    def copy_to_clipboard(self, text):
        """Copy text to clipboard and show confirmation"""
        if text:  # Only copy if there's text
            clipboard = QApplication.clipboard()
            # Extract just the number if the text is in format "SSIM Score: 0.1234"
            value = text.split(": ")[-1] if ": " in text else text
            clipboard.setText(value)
            
            # Store the original text from the label that corresponds to the button
            if self.sender() == self.ssim_copy_button:
                original_text = self.ssim_label.text()
            else:
                original_text = self.mse_label.text()
            
            # Create a timer to reset the button text
            timer = QTimer()
            timer.setSingleShot(True)
            
            # Determine which button was clicked
            if self.sender() == self.ssim_copy_button:
                self.ssim_label.setText(f"Copied: {value}")
                self.ssim_label.setStyleSheet("color: green;")
                self.ssim_copy_button.setText("Copied!")
                timer.timeout.connect(lambda: [
                    self.ssim_label.setText(original_text),
                    self.ssim_label.setStyleSheet(""),
                    self.ssim_copy_button.setText("Copy SSIM")
                ])
            else:
                self.mse_label.setText(f"Copied: {value}")
                self.mse_label.setStyleSheet("color: green;")
                self.mse_copy_button.setText("Copied!")
                timer.timeout.connect(lambda: [
                    self.mse_label.setText(original_text),
                    self.mse_label.setStyleSheet(""),
                    self.mse_copy_button.setText("Copy MSE")
                ])
            
            # Start the 2 second timer
            timer.start(2000)

    def check_files(self):
        if self.file1_path and self.file2_path:
            try:
                ssim_score, mse_score = compare_images(self.file1_path, self.file2_path)
                self.ssim_label.setText(f"SSIM Score: {ssim_score}")
                self.mse_label.setText(f"MSE Score: {mse_score}")
                # Show copy buttons when we have values
                self.ssim_copy_button.setVisible(True)
                self.mse_copy_button.setVisible(True)
            except Exception as e:
                self.ssim_label.setText(f"Error: {str(e)}")
                self.ssim_label.setStyleSheet("color: red;")
                # Hide copy buttons on error
                self.ssim_copy_button.setVisible(False)
                self.mse_copy_button.setVisible(False)

def main():
    app = QApplication(sys.argv)
    ex = SimpleApp()
    ex.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()