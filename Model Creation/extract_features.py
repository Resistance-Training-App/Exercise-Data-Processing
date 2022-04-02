import os, glob, sys
import pandas as pd
from math import floor

sys.path.append('../Tools')
sys.path.append('../Feature Extractions')
from selection import select_exercise
from format_df import format_df
from create_train_test_split import create_train_test_split
from bicep_curl import *
from lateral_raise import *
from shoulder_press import *
from exercise import *

import warnings
warnings.filterwarnings("ignore", category=FutureWarning) 

def process_data(exercise, folders):
    """
    Collects and extracts features from all types of motion including 'other' motion and saves to
    a dictionary where each key-value pair is a single type of motion.
    """

    motion_types = {}

    for folder in folders:

        # Iterate through each file in the folder.
        for filepath in glob.iglob(folder, recursive=True):
            if os.path.isfile(filepath) and filepath.split('.')[-1] == 'csv' and filepath.split('/')[4] != 'Test':
                df = pd.read_csv(filepath)

                # Adds an 'Activity' target column.
                df_formatted = format_df(df, filepath.split('/')[-1], exercise)

                # Divides the frame into discreate windows of data with an overlap.
                windows = create_windows(df_formatted)

                # Extracts features from each window and add to the motion dictionary.
                for window in windows:
                    add_to_motion_dict(exercise, window, motion_types)

                filename = filepath.split('/')[-1]
                print(f'Extracted features from {filename}')

    return motion_types

def add_to_motion_dict(exercise, window, motion_types):
    """
    Extracts features from a window of motion and adds the single row of data to the motion
    dictionary.
    """

    # Select feature extraction method based on the chosen exercise.
    if exercise == 'BicepCurl':
        row = bicep_curl(window)
    elif exercise == 'LateralRaise':
        row = lateral_raise(window)
    elif exercise == 'ShoulderPress':
        row = shoulder_press(window)
    elif exercise == 'Exercise':
        row = exercises(window)
    else:
        print(f'Could not find {exercise} feature extraction function.')
        exit()

    motion_type = row['activity']

    # Initially create an empty data frame if the motion has not been added to the dictionary
    # before.
    if motion_type not in motion_types:
        motion_types[motion_type] = pd.DataFrame()

    # Append the extracted features from the motion window to the motion dictionary.
    motion_types[motion_type] = motion_types[motion_type].append(row, ignore_index=True)

def create_windows(df):
    """
    Divides a long 2 minute training session of data into short 4 second windows of motion with a
    2 second overlap.
    """

    windows = []
    frequency = 40
    window_size = frequency * 4
    overlap = int(window_size * 0.5)
    num_windows = floor(df.shape[0] / overlap)

    # Iterate over the number of motion windows that need to be created.
    for window_index in range(0, num_windows-1):

        # Define the start and end indexes of the current motion window.
        start = window_index * overlap
        end = start + window_size

        # Create the window of data from the start and end indexes.
        window = df.iloc[start:end]
        windows.append(window)

    return windows

def main():

    # Pick an exercise to create the model for.
    exercise = select_exercise()

    # List of folders that contains the data needed for this model.
    folders = [f'../Exercises/{exercise}/Raw Data/**', '../Exercises/Other/Raw Data/Selected/**'] # All Data

    # Extracts features from the data and saves to a dictionary where each key-value pair is a
    # single type of motion.
    motion_types = process_data(exercise, folders)

    # Split data into train and test data frames with a split of 80% to 20% respectively.
    train, test, all_data = create_train_test_split(motion_types)

    # Save the training and testing data as separate CSV files.
    train.to_csv(f'../Exercises/{exercise}/Processed Data/train.csv', index=False)
    test.to_csv(f'../Exercises/{exercise}/Processed Data/test.csv', index=False)
    all_data.to_csv(f'../Exercises/{exercise}/Processed Data/all.csv', index=False)

    print(f'Train data saved to /Exercises/{exercise}/Processed Data/train.csv')
    print(f'Test data saved to /Exercises/{exercise}/Processed Data/test.csv')
    print(f'All data saved to /Exercises/{exercise}/Processed Data/all.csv')

if __name__ == '__main__':
    main()
