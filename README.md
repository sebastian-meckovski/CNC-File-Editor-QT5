# CNC File Editor
The CNC File Editor is a versatile tool tailored for efficient 
manipulation of .hop and .txt files, crucial for CNC machine 
operation.

### Purpose
This program automates routine changes, eliminating the need for
manual effort previously taking up an average of one hour per 
week for engineers. With just a few clicks, it streamlines file 
modifications, significantly reducing production costs.  For visual
demonstrations, please refer to the screenshots and video provided below.

### Key Features
- Batch Editing: Effortlessly make changes to a multitude of .hop and .txt files at once.
- Time Efficiency: Reduce the time spent on manual modifications, enhancing overall productivity.
- Cost Reduction: By streamlining the editing process, the CNC File Editor contributes to a decrease in production costs.

# Running the application
### Production environment

Run the .exe file included in the repo. The .exe file is packaged using pyinstaller, containing all dependencies. 
It's approximately 30MB in size, but the advantage is that it doesn't require installation. Requires Windows 7 or later.

### Development environment
NOTE: Ensure Python 3.9 is installed on your system. Versions later than 3.9 may not be compatible.
- In project root directory set up a virtual environment, by running
```commandline
python -m venv .\venv
```
- Activate Virtual Environment:
```commandline
.\venv\Scripts\activate
```
After activation, you should see **(venv)** on your terminal line.
- Install Dependencies:
```commandline
pip install -r requirements.txt
```
- Run the program
```commandline
python TextModifier.py
```
![CNC File Editor Screenshot](https://github.com/sebastian-meckovski/CNC-File-Editor-QT5/blob/master/media/Screenshot.png?raw=true)
[![CNC File Editor Demo](media/screenshot.png)](media/Video%20demonstration.mp4)
