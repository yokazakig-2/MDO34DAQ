# Test Environment
Oscilloscope : MDO34 3-BW-1000 (KEK ITDC Platform instruments #1)\
OS : Windows 10\
Terimnal : Command Prompt\
Python : 3.10.11\
TeKVISA : V4.1.1\
PyVISA : 1.15.0\
Connection from PC to Oscilloscope : USB cable (USB-A : PC, USB-B : Oscilloscope)\

# Setup
## Install Python
Skip or install from python web page (https://www.python.org/downloads/windows/)
## Install TekVISA
Install from Tektronix web page (https://www.tek.com/ja/support/software/driver/tekvisa-connectivity-software-v411)
## Install PyVISA
```
pip install pyvisa
```

# How to get waveform using trigger signal

## Default parameters
- Number of events : 10k
- Number of samples : 100k
- Time scale : 0.1 ms / div (i.e. full range is 1 ms.)
- Trigger point ; 50% on the display
- Record fist point : 1
- Record last point : 100k
- Trigger source : Ch1
- Trigger threshold : -0.4 V
- Trigger edge : Rising
- Waveform source : Ch1
- Data format : ASCII
- Amplitude data bit length : 16 bit
- Output file name : waveform\_screen.csv

# How to use
```
python get_waveform.py -h
```
You can check the options.
```
python get_waveform.py <options and arguments>
```
> Wait trigger signal\
> If oscilloscope receives a tigger signal, its status changes to STOP.\
> PC continues to checks the oscilloscope status until the status changes to STOP.\
> When PC confirms that the oscilloscope is in the STOP state, it reads out the waveform.\
> Once the reading is complete, the oscilloscope status changes to RUN.\
> Return to initial state\
