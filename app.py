import os
import uuid
from collections import Counter
import re
from flask import Flask, flash, request, redirect, render_template
import matplotlib.pyplot as plt
import numpy as np
import wave, sys
import pyaudioconvert as pac

UPLOAD_FOLDER = 'files'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def home():
    file_path = 'files/speech.txt'  # Replace with the path to your text file
    common_words = get_most_common_words(file_path)
    return render_template('index.html', list_to_send=common_words)


@app.route('/save-record', methods=['POST'])
def save_record():
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    file_name = str(uuid.uuid4()) + ".wav"
    full_file_name = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
    
    file_name = str(uuid.uuid4()) + "2.wav"
    full_file_name = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
    file.save(full_file_name)
    pac.convert_wav_to_16bit_mono(full_file_name, full_file_name)
    return '<h1>Success</h1>'

def get_most_common_words(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    # Convert all words to lowercase and extract words using regular expression
    words = re.findall(r'\b\w+\b', text.lower())

    # Count the occurrences of each word
    word_counts = Counter(words)

    # Get the 10 most common words
    most_common_words = word_counts.most_common(10)

    return most_common_words

def visualize(path: str):
   
    # reading the audio file
    raw = wave.open(path)
     
    # reads all the frames 
    # -1 indicates all or max frames
    signal = raw.readframes(-1)
    signal = np.frombuffer(signal, dtype ="int16")
     
    # gets the frame rate
    f_rate = raw.getframerate()
 
    # to Plot the x-axis in seconds 
    # you need get the frame rate 
    # and divide by size of your signal
    # to create a Time Vector 
    # spaced linearly with the size 
    # of the audio file
    time = np.linspace(
        0, # start
        len(signal) / f_rate,
        num = len(signal)
    )
 
    # using matplotlib to plot
    # creates a new figure
    plt.figure(1)
     
    # title of the plot
    plt.title("Sound Wave")
     
    # label of x-axis
    plt.xlabel("Time")
    
    # actual plotting
    plt.plot(time, signal)
     
    # shows the plot 
    # in new window
    plt.show()
 
    # you can also save
    # the plot using
    # plt.savefig('filename')

if __name__ == '__main__':
    file_path = 'files/speech.txt'  # Replace with the path to your text file
    common_words = get_most_common_words(file_path)

    print("Top 10 most common words (case-insensitive):")
    for word, count in common_words:
        print(f"{word}: {count} times")
    
    # path = 'files/test.wav'
 
    # visualize(path)

    app.run()