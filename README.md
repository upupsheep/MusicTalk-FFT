# MusicTalk-FFT

**MusicTalk-FFT** used a script to analysis frequency information and onset information from a wav file. Then it used **IoTTalk** to map those frequency information to color and to push these color information to other output devices.

### 1. Usage:

Make sure you install all the python dependency.

This project uses `librosa` and `scipy`. To install `librosa`, use the following command:

```=shell
pip install librosa
```

To install `scipy`, use the following command:

```=shell
pip install scipy
```

Also, make sure you have `DAN.py`, `csmapy.py` in the same directory.

Change the `filepath` in the code (on line `10`) to the wav file you want.

For example:(on line `10`)

```=python
file_path = "night.wav"
```

Finally, run the program using the following command:

```=bash
python music_with_beats.py
```

If connecting with IoTTalk, run this command to start IDF program:

```=bash
python beat_dai.py
```



