Documentation for Waveform GUI
------------------------------
Files found at: https://github.com/pdanPOLY/Waveform-GUI

Inital Setup
------------
-Download any of the recent version of Python (make sure you choose to install pip with it)
-(Recommended) Download Visual Studio Code as a text editor for code with a convenient terminal menu
-Once you have the file with all the code (gui2.py), put it in a folder in some accessible place such as 
 your desktop, and open that folder through VS Code
-NOTE: The files can directly be double clicked on and opened with python, but it doesn't let you see the code and edit it
-EXCEL FILE LOCATION: The excel files will be saved to the same location as the python program, so it is recommended to put them in a folder together

Imports
-------
-PySimpleGui is the library you need to import in order to easily 
 develop the layout for the GUI.
	-Installation: Enter "pip install pysimplegui" (or "py -m pip install pysimplegui") in the command prompt
-pySerial is the library you need for serial communication between python and a microcontroller
 through COM ports.
	-Installation: Enter "pip install pyserial" (or "py -m pip install pyserial") in the command prompt
-pandas has a lot of different features, and we will be needing the DataFrame object for convenient data formatting
	-Installation: Enter "pip install pandas" (or "py -m pip install pandas") in the command prompt
	-Additionally, must do "pip install openpyxl" (or "py -m pip install openpyxl") in the command prompt for saving the data into an excel file
-datetime simply helps you retrieve the current date and time, so that you can have a time stamp for when the file was saved
	-Installation: Enter "pip install datetime" (or "py -m pip install datetime") in the command prompt

Code Functionality
------------------
-The first section of the program sets up all the layout for the GUI that we need
	-The GUI is set so that clicking submit will process all the info and try to send it serially
	-The GUI will only close if the program ends or the exit button is clicked
	-Pressing submit will allow you to continually click submit with whatever values you would like
-The methods "generateInfo" and "generateInfo2" pass in the values from all the inputs on the GUI,
 and use those values to return a dictionary of information that is more accessible and understandable
-Once the data is generated, "assertRanges" and "assertRanges2" will parse through all the data
 and make sure the inputted data was in the accepted ranges
	-If any of the data was inputted incorrectly, the error will be caught and the program will end
-The data gets sent serially to the microcontroller, and then reads the resistance values and saves them to an excel file
 (Must check that correct COM port is connected: connect your microcontroller, and where the serial connection is set up at the bottom 
  of the code, replace the "COM9" parameter with your desired communication port, and fill out the rest of the parameters correspondingly.)

Running the Program
-------------------
-Once in VS Code in the folder where the Python file is located, click on the "Terminal" tab
 at the top of the screen and open a new terminal
-In the new terminal, make sure that the destination is the correct folder and it is using Powershell
	-If the destination is incorrect for some reason, use the commands "cd .." to move back a folder, 
	 and "cd Desktop" to move forward to your Desktop for example
-Once in the correct location, enter the command "python gui2.py" (or "py gui2.py" if the previous doesn't work)
	-You should see a drop down with two different programming options --> select one and press submit
-SINGLE DEVICE PROGRAMMING:
	-First Stage must be completely filled out
	-If an option for any of the other stages is selected, all the values for it must be filled out (except for Read)
	-Row and Column must be filled out (1-8 for both)
	-Number of repetitions defaults to 1, but accepted range is 1-125
	-Accepted range for all the Time/Blank Period fields is 1-125 (Time defaults to 1 for Forming)
	-Accepted range for Voltage fields is -2.5V to 2.5V, but must be left as 3.3V for Forming (Read voltages are limited to negatives and 0)
-SINGLE COLUMN PROGRAMMING:
	-The set/reset fields need to be filled out, but the read fields don't need to be filled out
	-Row Bit data (defaults to all 1s) and column must be filled out
	-Time/Blank Period ranges 1-125
	-Voltage ranges -2.5V to 2.5V (Read voltages are limited to negatives and 0)
	-Row Bit data must be 0 or 1, and from left to right is Rows [1,2,...,8] (1 refers to Set, 0 refers to Reset)
	-Column ranges 1-8
-To close the GUI, hit the X in the top right
