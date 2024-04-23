# README

Python script that gets input from a zeromq stream from a Furhat device and sends it as an annotated video stream to a virtual camera (v4l2loopback).

On Linux, do this (replace X.X.X.X with an appropriate IP number):
```(bash)
python3 -m venv ~/furhat.venv
source ~/furhat.venv/bin/activate
pip3 install -r requirements.txt
./create_virtual_camera_device.sh
python3 furhattube.py X.X.X.X
```

Now, open obs-studio and add a "Video Capture" device. Choose the virtual camera to capture the stream.

Use Ctrl-C to stop the script.

And, when you are done, you may remove the virtual camera device, if you want with:

```(bash)
./remove_virtual_camera.sh
```