Software requirements: Python v3.7.9

Installation:

1. Download the project repository (Click on the Code green button / Download Zip)

2. Copy SensorComparison to a newly created C:\Tools folder

3. Install Python v3.7.9 from C:\Tools\SensorCompare\Software\python-3.7.9-amd64.exe

4. Browse to C:\Tools\SensorCompare and right click the Install.bat and open with Notepad ++ or Notepad

5. Browse to the location on your pc where Python has been installed. Choose the Python\Python37\Scripts location and copy the path of this location. The pip.exe file within this location will download additional libraries required for the application to function.

6. Within Install.bat, replace the default path on Line 1 with the path you just copied from your local machine.

7. Save Install.bat

8. Save and close Install.bat

9. Double click Install.bat to install the python Libraries

10. Starting Script:

    a. Right Click on Datalogger_Processing_V1.1.py

    b. Select Edit with Idle 3.7 (64 bit)
  
    ![image](https://github.com/HydroPanadas/SensorCompairson/assets/80972086/aa21ad19-4a8e-451f-a6df-e76b23368f8c)
  
    c. File Menu- Select Run – Run Module or F5
  
    ![image](https://github.com/HydroPanadas/SensorCompairson/assets/80972086/15abb123-31fb-420c-9b95-1901a5c296f5)

  d. Specify Start and End Date and Time. (This will be the extents you would like to compare the testing sensors with the Calibration sensor (Laser Sensor from Station 0491)
  
  e. Specify the Folder location for the Calibration Sensor (WLO File), and the Testing Sensor(s) 8310 Log File.
  
  f. Select the Sensor Tidal measurements you would like to compare.
  
  g. Ensure the correct threshold is choosen. (3cm for OTT Preassure Sensors)

  h. Specify the Serial Numbers for each tidal Measuement. This will be used for file nameing and folder management
  
  h. Graphs will be created and saved in a designated folder within the Script Folder. (Make sure to copy these to a new location)
  

