import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout

# Define a custom class for the main window
class SimpleApp(QWidget):
    def __init__(self):
        super().__init__()

        # Set up the window
        self.setWindowTitle("PyQt Simple Application")
        self.setGeometry(100, 100, 300, 200)  # (x, y, width, height)

        # Initialize the layout
        layout = QVBoxLayout()

        # Create a label widget
        self.label = QLabel("Hello! Click the button below.", self)
        layout.addWidget(self.label)

        # Create a button widget
        self.button = QPushButton("Click Me!", self)
        self.button.clicked.connect(self.on_button_click)  # Connect button click to a function
        layout.addWidget(self.button)

        # Set the layout for the main window
        self.setLayout(layout)

    # Define what happens when the button is clicked
    def on_button_click(self):
        self.label.setText("Button Clicked! Welcome to PyQt!")

# Boilerplate code to run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)  # Create an instance of the application
    window = SimpleApp()           # Create an instance of the window
    window.show()                  # Show the window
    sys.exit(app.exec_())          # Run the application's main loop
