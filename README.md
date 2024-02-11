# Stepmania Songpack Control

## Overview

This Python script provides functionality to manage songpacks for Stepmania. It allows users to generate a hash cache for all files within specified directories, enabling the identification of duplicate files and folders. Additionally, it offers the option to delete the duplicates.

Should be ran in admin since deleting files often create an issue with permissions.

## Features

- Hash Cache Generation: Creates a hash cache for all files within specifieddirectories recursively.
- Duplicate Detection: Identifies duplicate files based on their hash values.
- Interactive User Interface: Utilizes an interactive command-line interface to prompt users for actions.
- Duplicate File Deletion: Provides the option to delete duplicate files,prioritizing the retention of the oldest file.
- Validation: Ensures the integrity of the hash cache upon loading by validating file paths.
- Progress Tracking: Displays a progress bar during the hash cache generationprocess.

## Prerequisites

- Python 3.x
- tqdm (for progress bar) (`pip install tqdm`)
- Stepmania installation (for songpack management)

## Usage

    Clone the repository to your local machine.
    Navigate to the directory containing the script.
    Run the script using Python: python main.py.
    Follow the on-screen instructions to generate the hash cache and manage songpacks.

## Important Notes

   - Ensure proper permissions for file deletion operations, especially on Windows systems.
   - Exercise caution when deleting duplicate files, as irreversible data loss may occur.

## License

This project is licensed under the MIT License. See the LICENSE file for details.