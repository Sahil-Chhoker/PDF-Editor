# File Converter Tool

This Python script provides a graphical user interface (GUI) for performing various operations on text and PDF files. It allows users to convert text files to PDF, split PDFs, merge PDFs, convert PDFs to images, and convert PDFs to PowerPoint presentations.

## Dependencies

Ensure you have the following dependencies installed:

- tkinter: Python's standard GUI (graphical user interface) toolkit.
- os: Provides a portable way of using operating system-dependent functionality.
- shutil: Provides a higher-level interface for file operations.
- filedialog from tkinter: Provides dialogs for opening and saving files.
- pathlib: Provides classes representing filesystem paths.
- fpdf: A Python library for generating PDF files.
- PyPDF2: A Python library to work with PDF files.
- pdf2image: A Python library to convert PDFs to images.
- dotenv: A Python library to manage environment variables.
- groupdocs_conversion_cloud: A Python library for converting documents, powered by GroupDocs.

## Setup

1. Clone this repository to your local machine.

2. Install the required dependencies using pip:

```
pip install -r requirements.txt
```

3. Set up environment variables for authentication with the GroupDocs API. Create a `.env` file in the root directory of the project and add your client ID and client secret. (For more information on getting your credentials visit https://dashboard.groupdocs.cloud/) :

```
CLIENT_ID=your_client_id_here
CLIENT_SECRET=your_client_secret_here
```

## Usage

1. Run the script by executing `python main.py` in your terminal.
2. The GUI window will open, allowing you to perform various file conversion operations.
3. Click on the desired operation button to perform the corresponding action.
4. Follow the on-screen instructions to select input files and output directories.

## Author

Sahil Chhoker
