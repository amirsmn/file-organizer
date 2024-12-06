# File Organizer

A Python-based tool for organizing files into categorized folders based on their extensions. It automates file management by moving files into appropriate directories and handles various error scenarios.

## Introduction 

**File Organizer** simplifies file management by automating common tasks such as retrieving, creating, and moving files. It ensures hidden files (those starting with '.') are excluded from operations by default.

This project helps organize files in a directory structure, improving consistency and efficiency. It provides easy-to-use methods with built-in error handling and logging for better tracking and debugging.

## Features

* Automatically organizes files into folders based on their extension.
* Handles various types of files, including images, documents, audio, videos, and more.
* Supports customizable folder mappings via a JSON configuration file.
* Detailed logs for easier tracking and debugging.
* Files with unsupported extensions are placed in a folder named **OTHERS** (or any folder you prefer).
* Organize multiple folders in a single execution.

## Usage

To use the File Organizer, follow these steps:

**1. Clone the repository:**

```bash
git clone https://github.com/amirsmn/file-organizer.git
```

**2. Navigate to the project directory:**

```bash
cd file-organizer
```

**3. Install dependencies:**

```bash
pip install -r requirements.txt
```

**4. To run the project, execute the following command:**

```bash
python -m scripts.main <arguments> [options]
```

- For detailed usage instructions or to view available options, run:

```bash
python -m scripts.main -h
```

## Contributing

Feel free to submit issues or pull requests if you'd like to contribute to this project. Suggestions for new features or improvements are always welcome! :slightly_smiling_face: