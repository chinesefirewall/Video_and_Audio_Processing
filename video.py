# Importing the required libraries
import os
import scipy.io.wavfile as wavfile
import numpy as np
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip as exr
import subprocess

# Define the folder numbers to be processed
folder_number = np.arange(1,2)

# Loop through each folder
for num in folder_number:
    print("Processing folder number: ", num)

    # Define the directory path where the split files are located
    dir = os.path.join('/media/icv/The Boss/split','split{}'.format(num))

    # Change the working directory to the target directory
    os.chdir(dir)

    files = []

    # Loop through each file in the directory
    # r=root, d=directories, f = files
    for r, d, f in os.walk(dir):
        for file in f:
            if '.mp4' in file:
                files.append(file)

    # Loop through each .mp4 file
    for f in files:
        f = f.rstrip('mp4')
        print(f)

        # Extract the audio from the .mp4 file
        aud_sep = subprocess.Popen("ffmpeg -i {}mp4 -vn -codec:a libmp3lame {}1.mp3".format(f, f), shell=True)
        aud_sep.communicate()

        # Wait until the audio file is available
        while True:
            try:
                open(f+'1.mp3')
                break
            except:
                continue

        # Denoise the audio using sox
        denoise = subprocess.Popen('sox {} -n trim 1 1 noiseprof| sox {} {} noisered'.format(f+'1.mp3',f+'1.mp3',f+'2.mp3'), shell=True)
        denoise.communicate()

        # Wait until the denoised audio file is available
        while True:
            try:
                open(f+'2.mp3')
                break
            except:
                continue

        # Normalize the audio using sox
        normalise = subprocess.Popen('sox {}2.mp3 {}3.mp3 norm'.format(f,f), shell=True)
        normalise.communicate()

        # Wait until the normalized audio file is available
        while True:
            try:
                open(f+'3.mp3')
                break
            except:
                continue

        # Convert the normalized audio file to .wav format
        mp3_to_wav = subprocess.Popen('ffmpeg -i {}3.mp3 {}wav'.format(f,f), shell=True)
        mp3_to_wav.communicate()

        # Wait until the .wav file is available
        while True:
            try:
                open(f+'wav')
                break
            except:
                continue

        # Read the .wav file and convert stereo audio to mono
        fs_rate, signal = wavfile.read(f+'wav')
        if len(signal.shape) == 2:
            signal = signal.sum(axis=1) / 2

        # Determine the time of the last peak in the audio signal
        last_peak = np.argwhere(signal > 10000)[-1]
        time = last_peak[0] / fs_rate + 1.4

        # Trim the .mp4 file to start from the time of the last peak
        exr(f+'mp4', time, signal.shape[0]/fs_rate, '/media/icv/nash/Niyi/major_trim{}/'.format(num) +f+'mp4')
