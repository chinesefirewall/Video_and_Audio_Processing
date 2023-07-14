# Video_and_Audio_Processing

Video and Audio Processing Script
This Python script processes video and audio files. It is designed to handle .mp4 video files and extract, process, and normalize the audio tracks from them.

Requirements
The script uses the following external libraries:

os
scipy
numpy
moviepy
subprocess
Moreover, it relies on the following tools that should be installed in your system:

ffmpeg
sox
What the script does
The script works as follows:

It loops through each directory labeled numerically from 1 to n (you can modify this in the folder_number variable).
For each directory, it switches the working directory to it and searches for all .mp4 files in that directory and its subdirectories.
For each .mp4 file, the script uses ffmpeg to extract the audio track and save it as an .mp3 file.
It then uses sox to reduce noise in the audio and normalize the volume.
After the audio has been denoised and normalized, the script converts the .mp3 audio file back to a .wav format.
The script reads the .wav file to obtain the sample rate and the audio signal data. If the audio is stereo (2 channels), it averages the two channels to make it mono.
It identifies the locations in the audio signal where the signal strength exceeds a certain threshold (10000 in this case). It retrieves the time at which the last such peak occurs.
Finally, the script trims the original .mp4 video file to start from 1.4 seconds after the last peak in the audio signal, and saves the trimmed video in a specified directory.
How to use
You should specify the range of folder numbers to be processed in the folder_number variable.

You also need to adjust the directory paths (dir and the output path in the exr function) according to your system setup.

Run the script and it will process all .mp4 files in the specified folders, one by one.