import argparse
import sys

from PyQt5.QtWidgets import QApplication

from EDLParser import EDLParserApp

if __name__ == "__main__":
    """
    Main Function.

    Main function which initializes the EDL Parser application, creates the application window and shows it to end user.
    
    Args:
        None

    Returns:
        None
    """
    app = QApplication(sys.argv)
    window = EDLParserApp()
    window.show()
    sys.exit(app.exec_())
