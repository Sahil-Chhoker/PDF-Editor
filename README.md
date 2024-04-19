# PDF Editor

This Python script provides a graphical user interface (GUI) for performing various operations on text and PDF files. It allows users to convert text files to PDF, split PDFs, merge PDFs, convert PDFs to images, and convert PDFs to PowerPoint presentations.

## Features

- Convert text files to PDF format
- Split PDF files into multiple PDFs
- Merge multiple PDF files into a single PDF
- Convert PDF files to image format (PNG, JPG, etc.)
- Convert PDF files to PowerPoint presentations

## Dependencies

Ensure you have the following dependencies installed:

- **tkinter**: Python's standard GUI (graphical user interface) toolkit.
- **os**: Provides a portable way of using operating system-dependent functionality.
- **shutil**: Provides a higher-level interface for file operations.
- **filedialog** from tkinter: Provides dialogs for opening and saving files.
- **pathlib**: Provides classes representing filesystem paths.
- **fpdf**: A Python library for generating PDF files.
- **PyPDF2**: A Python library to work with PDF files.
- **pdf2image**: A Python library to convert PDFs to images.
- **dotenv**: A Python library to manage environment variables.
- **groupdocs_conversion_cloud**: A Python library for converting documents, powered by GroupDocs.

## Setup

1. Clone this repository to your local machine.

```bash
git clone https://github.com/Sahil-Chhoker/PDF-Editor.git
```

2. Create a virtual environment (optional but recommended).

```bash
python -m venv env
source env/bin/activate  # On Windows, use `env\Scripts\activate.ps1`
```

3. Navigate to the project directory.

```bash
cd PDF-Editor
```

4. Install the required dependencies using pip.

```bash
pip install -r requirements.txt
```

5. Set up environment variables for authentication with the GroupDocs API. Create a `.env` file in the root directory of the project and add your client ID and client secret. (For more information on getting your credentials, visit https://dashboard.groupdocs.cloud/)

```
CLIENT_ID=your_client_id_here
CLIENT_SECRET=your_client_secret_here
```

## Usage

1. Run the script by executing `python main.py` in your terminal.
2. The GUI window will open, allowing you to perform various file conversion operations.
3. Click on the desired operation button to perform the corresponding action.
4. Follow the on-screen instructions to select input files and output directories.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Author

Sahil Chhoker
