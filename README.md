# Python Word Similarity Analysis

This program processes any given `.wav` signal (or records a signal via input) and creates its respective LPC and MFCC vectors, with configurable params. It then calculates the similarity between inputs through DTW.

## Author

[![Author](https://andrejanesic.com/git-signature.png)](https://github.com/andrejanesic)

This project is largely based on the code/information provided by the following resources and their respective authors:

- [Linear Predictive Coding, kunigami, 11 Dec 2021](https://github.com/kunigami/kunigami.github.io/blob/master/blog/code/2021-05-13-lpc-in-python/lpc.ipynb)
- [LPC_Speech_Synthesis](https://github.com/hcy71o/LPC_Speech_Synthesis/blob/develop/Speech_analysis.ipynb)
- [StackOverflow: "Writing WAV file using Python, Numpy array and WAVE module"](https://stackoverflow.com/questions/40782159/writing-wav-file-using-python-numpy-array-and-wave-module)
- [vanilla-stft-mfcc](https://github.com/brihijoshi/vanilla-stft-mfcc/blob/master/notebook.ipynb)

## Setup & Running

This is a command-line Python program. Python 3 is necessary to run. It is also possible to run this program via the given Dockerfile (through Makefile), however, you'll need to modify the Makefile to include a display port for Docker in order to see Pyplot graphs. It's recommended to run this program directly on your computer without Docker.

### Setup On Local Computer

To run this program on your local computer, execute the following Git command:

```
git clone https://github.com/andrejanesic/Python-Word-Similarity-Analysis.git
```

This will clone the repository onto your local computer.

This program requires Python, so if it isn't installed on your computer, you can download it from the [Python.org website.](https://www.python.org/downloads/)

Next, install the required libraries for Python using pip:

```
pip install -r requirements.txt
```

You're good to go!

## Task Specification

This program was developed as an individual assignment for the class of [[5025] Speech Recognition](https://raf.edu.rs/en/component/content/article/192-english/subjects/3359-speech-recognition), cohort 2022/23, at the [School of Computing, Union University, Belgrade.](https://rs.linkedin.com/school/racunarski-fakultet/)

### Task Description

_#TODO_