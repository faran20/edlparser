import re
import os
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem, QPushButton, \
    QVBoxLayout, QWidget, QFileDialog, QLineEdit, QHBoxLayout


class EDLParserApp(QMainWindow):
    """
    EDLParserApp class for parsing and processing EDL files.

    Class to create the graphical user interface for end user to open any EDL file and processed data will be shown
    on the window.
    """

    def __init__(self):
        """
        Initialize the EDLParserApp GUI.

        Constructor is to set the main components of GUI, calls the user interface function to initialize and also
        defines the clip_data list for storing the data required to present on the GUI.

        Attributes:
        - central_widget (QWidget): The central widget of app.
        - layout (QVBoxLayout): The main layout of app.
        - horizontal_layout (QHBoxLayout): The horizontal layout for organizing items horizontally
        - table_widget (QTableWidget): The table widget for displaying data in the tabular form.
        - text_edit (QLineEdit): The text bar widget for address bar.
        - open_button (QPushButton): The button for opening EDL files.
        - generate_button (QPushButton): The button to generate or executing action defined in the function.

        clip_data (list): A list for storing data required to present on the GUI.

        Returns:
            None
        """
        super().__init__()

        # Main components of the GUI
        self.central_widget = None
        self.layout = None
        self.horizontal_layout = None
        self.table_widget = None
        self.text_edit = None
        self.open_button = None
        self.generate_button = None

        # Calling function to create the GUI
        self.create_ui()

        # List of the data required to present on GUI
        self.clip_data = []

    def create_ui(self):
        """
        To create the user interface for EDL Parser app.

        This function is to set the layout, widgets, and set the coordinates where required.

        Returns:
            None
        """
        # Set title and size of the window
        self.setWindowTitle("EDL Parser")
        self.setGeometry(100, 100, 800, 600)

        # Setting the widget to central widget
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Creating the layout for items to be shown in vertical view
        self.layout = QVBoxLayout()

        # Creating the layout for horizontal items
        self.horizontal_layout = QHBoxLayout()

        # Create and configure the address text bar (LineEdit)
        self.text_edit = QLineEdit(self)
        self.text_edit.setFixedWidth(int(0.7 * self.width()))

        # Create and configure the "Open EDL File" button
        self.open_button = QPushButton('Open EDL File', self)
        self.open_button.setFixedWidth(int(0.2 * self.width()))
        self.open_button.clicked.connect(self.open_file)

        # Adding the address bar and file opening button to Horizontal Layout
        self.horizontal_layout.addWidget(self.text_edit)
        self.horizontal_layout.addWidget(self.open_button)
        self.horizontal_layout.setStretch(0, 8)  # Seting stretch for address bar
        self.horizontal_layout.setStretch(1, 2)  # Seting stretch for button
        self.layout.addLayout(self.horizontal_layout)

        # Setting the tabular view for items to load with default header and column count
        self.table_widget = QTableWidget(self)
        self.table_widget.setColumnCount(4)
        self.table_widget.setHorizontalHeaderLabels(["Clip", "Shot", "Episode", "Season"])
        self.layout.addWidget(self.table_widget)

        # Create and configure the "Generate Folders" button
        self.generate_button = QPushButton("Generate Folders", self)
        self.generate_button.setFixedWidth(int(0.2 * self.width()))
        self.generate_button.clicked.connect(self.generate_folders)

        # Setting up the Generate button position on layout.
        self.horizontal_layout = QHBoxLayout()
        self.horizontal_layout.addWidget(self.generate_button)
        self.horizontal_layout.setAlignment(self.generate_button, Qt.AlignRight)

        # Adding layout back to the main layout
        self.layout.addLayout(self.horizontal_layout)

        # Adding layout to the central widget
        self.central_widget.setLayout(self.layout)

    def open_file(self):
        """
        Open and process an EDL file.

        Function is to pop up the dialogue for file selection and if file selected, it's address will be shown in the
        text bar available on GUI. If file is valid, then it sent to parser function.

        If the file extension is not .edl or user didn't select any file then no action will be performed.

        Raises:
        FileNotFoundError: If the selected file does not exist or is not accessible.

        Returns:
            None
        """
        # Setting the options to load file from system.
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly

        try:
            # Setting the dialogue to open only EDL files or all kind of files
            filename, _ = QFileDialog.getOpenFileName(self, "Open EDL File", "", "EDL Files (*.edl);;All Files (*)",
                                                      options=options)
            # Conditional processing if file is ending with required extension.
            if str(filename).endswith('.edl'):
                self.text_edit.setText(filename)  # setting address value into the address bar
                self.parse_edl_file(filename)  # calling parser function to process the file

        except FileNotFoundError:
            raise FileNotFoundError(f"The file does not exist or is not accessible.")

    def parse_edl_file(self, edl_file):
        """
        Process an EDL file.

        Function to read the data available in given file and perform different actions on it to extract the
        required content out of it.

        Parameters:
            edl_file (str): The path to the EDL file to be processed.

        Raises:
            IOError: If an error occurs while reading the file.

        Returns:
            None
        """

        try:
            pattern = r'^s\d{2}e\d{2,3}$'  # Regular expression to filter data

            with open(edl_file, 'r') as file:  # Reading file with Mode 'R'
                for line in file:  # Iterating through all lines in the loaded file
                    if line.strip().startswith("REEL"):  # Selecting the string starting with REEL
                        clip_name = line.split("CLIP")[1].strip()  # Splitting the string with CLIP
                        parts = clip_name.split("_")

                        # Filtering the data using patterns and then extracting required data
                        if re.match(pattern, parts[0]):
                            season = parts[0][0:3]
                            episode = parts[0][3:]
                            shot = ''

                            # Checking if the padding for episode number is less than 3
                            if len(episode) <= 3:
                                e_number = episode.split('e')[1]
                                e_number = e_number.zfill(3)
                                episode = f"e{e_number}"

                            # Condition if the line ending with MOV extension
                            if parts[len(parts) - 1].endswith(".mov"):
                                shot = parts[4].split("-")[1]
                                shot = shot.split(".")[0]
                                shot = shot.zfill(4)
                                shot = f"{episode}s{shot}"

                            # Condition to check if line ending with WAV extension
                            if parts[len(parts) - 1].endswith(".wav"):
                                shot = parts[1].split("-")[0]
                                shot = shot.zfill(4)
                                shot = f"{episode}s{shot}"

                            # Adding the tuple into the list
                            self.clip_data.append((clip_name, shot, episode, season))
            self.load_edl_data()
        except IOError as e:
            raise IOError(f"An error occurred while reading the file '{edl_file}': {str(e)}")

    def load_edl_data(self):
        """
        Load and display the data.

        Function is to add data into the table view for end user to view on GUI

        Returns:
            None
        """
        # Create number of rows based on the size of list
        self.table_widget.setRowCount(len(self.clip_data))

        # Iterate through list to set data row by row
        for row, data in enumerate(self.clip_data):
            # Iterate through tuple of strings to set values in column
            for col, item in enumerate(data):
                self.table_widget.setItem(row, col, QTableWidgetItem(item))  # setting the item value in widget

    def generate_folders(self):
        """
        Generate folder structure.

        As per the EDL hierarchy, this function creates the directories and subdirectories based on the extracted
        information out of the EDL data.

        Returns:
            None
        """
        #  Setting the current directory as a base directory
        base_directory = os.getcwd()

        # Iterate through the file information list
        for file_info in self.clip_data:
            file_name, shot_folder, episode_folder, season_folder = file_info

            # Create the season directory if it doesn't exist
            season_directory = os.path.join(base_directory, season_folder)
            if not os.path.exists(season_directory):
                os.makedirs(season_directory)

            # Create the episode directory within the season directory
            episode_directory = os.path.join(season_directory, episode_folder)
            if not os.path.exists(episode_directory):
                os.makedirs(episode_directory)

            # Create the shots directory within the episode directory
            shot_directory = os.path.join(episode_directory, shot_folder)
            if not os.path.exists(shot_directory):
                os.makedirs(shot_directory)

        print("Folders created successfully.")
