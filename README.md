
# Weight and Volume Monitoring System (WaV) by COCOO

## Overview
The Weight and Volume Monitoring System (WaV) by COCOO is a Python application designed to monitor and record weight and volume data of parcels. It interfaces with a weighing machine and captures data from parcels in real-time. The application allows users to input data manually or automatically, retrieve data from a connected machine, and download recorded data for analysis.

## Features
- **Manual Input**: Users can input data manually including system ID, weight, height, length, and width of parcels.
- **Automatic Data Capture**: The application automatically captures data from a connected weighing machine, providing real-time updates.
- **QR Code Scanner**: Integration with a QR code scanner allows for easy input of system IDs.
- **Data Recording**: Recorded data is stored in an Excel file for future reference and analysis.
- **Total Weight and Volume Calculation**: The application calculates and displays the total weight and volume of all recorded parcels.
- **User Interface**: The graphical user interface (GUI) provides an intuitive way to interact with the application.

## Installation
1. Clone the repository to your local machine.
2. Install the required Python packages using `pip install -r requirements.txt`.
3. Connect the weighing machine to your computer.
4. Run the `main.py` file to launch the application.

## Usage
1. Launch the application by running `main.py`.
2. Choose the appropriate COM port for the weighing machine connection.
3. Select the webcam if necessary.
4. Use the "AUTO" button to automatically capture data from the weighing machine.
5. Alternatively, input data manually using the provided fields.
6. Click on the "GET" button to manually capture data from the weighing machine.
7. Recorded data will be displayed in the GUI and stored in an Excel file.
8. Use the "Download" button to download recorded data for analysis.

## Dependencies
- Python 3.x
- pandas
- tkinter
- pyserial
- OpenCV
- PIL (Python Imaging Library)

## Authors
- omar faruk ruman
