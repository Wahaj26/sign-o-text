# Sign-o-text
A Beginner level Application which translate sign language into text or voice (with using extra hardware just need your laptop camera or any other camera) using python OpenCv & Keras api's (machine learning &amp; image processing) helpfull for beginner's.

## What I did here
1. The first thing I did was, I created 44 gesture samples using OpenCV. For each gesture I captured 1200 images which were 50x50 pixels. All theses images were in grayscale which is stored in the gestures/ folder. The pictures were flipped using flip_images.py. This script flips every image along the vertical axis. Hence each gesture has 2400 images.
2. Learned what a CNN is and how it works. Best resources were <a href="https://www.tensorflow.org/get_started/">Tensorflow's official website</a> and <a href="https://machinelearningmastery.com">machinelearningmastery.com</a>.
3. Created a CNN which look a lot similar to <a href="https://www.tensorflow.org/tutorials/layers">this MNIST classifying model</a> using both Tensorflow and Keras. If you want to add more gestures you might need to add your own layers and also tweak some parameters, that you have to do on your own.
4. Then used the model which was trained using Keras on a video stream.
5. As of today, I have created 3 4 different models, like one for words gestures, one for letters & others for actions words gesture.

There are a lot of details that I left. But these are the basic and main steps.

## Requirements
0. Python 3.x
3. OpenCV 3.4
4. h5py
5. pyttsx3
6. kivy
7. A good grasp over the above 5 topics along with neural networks. Refer to the internet if you have problems with those. I myself am just a begineer in those.
8. A good CPU (preferably with a GPU).

## How to use this repo
After clone this repo, install all requirements mention above & simply run `python index.py` in terminal.
A GUI appears click start, then you see multiple options one for letter conversion & other for words conversion you may check both.

# Got a question?
If you have any questions that are bothering you please contact me on my <a href = "https://www.facebook.com/qwahaj1">facebook profile</a>.
