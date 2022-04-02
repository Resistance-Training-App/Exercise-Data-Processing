import pandas as pd
import matplotlib.pyplot as plt
from math import pi
from selection import *

import numpy as np

def display_data(data, data_name):
    """Plots all motion data, useful for finding features to extract and general debugging."""

    # Rotation Rate
    plt.figure(data_name + ' - Rotation Rate')
    plt.plot(data.TimeStamp.to_list(), data.DMRotX.to_list(), label='X')
    plt.plot(data.TimeStamp.to_list(), data.DMRotY.to_list(), label='Y')
    plt.plot(data.TimeStamp.to_list(), data.DMRotZ.to_list(), label='Z')
    plt.xlabel('Time [s]')
    plt.ylabel('Angular Velocity [rad/s]')
    plt.legend()

    # Acceleration
    plt.figure(data_name + ' - Acceleration')
    plt.plot(data.TimeStamp.to_list(), data.DMUAccelX.to_list(), label='X')
    plt.plot(data.TimeStamp.to_list(), data.DMUAccelY.to_list(), label='Y')
    plt.plot(data.TimeStamp.to_list(), data.DMUAccelZ.to_list(), label='Z')
    plt.xlabel('Time [s]')
    plt.ylabel('Acceleration [m/s^2]')
    plt.legend()

    # Gravity
    plt.figure(data_name + ' - Gravity')
    plt.plot(np.convolve(data.TimeStamp.to_list(), np.ones(10)/10, mode='valid'),
             np.convolve(data.DMGrvX.to_list(), np.ones(10)/10, mode='valid'), label='X')
    plt.plot(np.convolve(data.TimeStamp.to_list(), np.ones(10)/10, mode='valid'),
             np.convolve(data.DMGrvY.to_list(), np.ones(10)/10, mode='valid'), label='Y')
    plt.plot(np.convolve(data.TimeStamp.to_list(), np.ones(10)/10, mode='valid'),
             np.convolve(data.DMGrvZ.to_list(), np.ones(10)/10, mode='valid'), label='Z')
    plt.xlabel('Time [s]')
    plt.ylabel('Gravity')
    plt.legend()

    # Quaternion
    plt.figure(data_name + ' - Quaternion')
    plt.plot(data.TimeStamp.to_list(), data.DMQuatX.to_list(), label='X')
    plt.plot(data.TimeStamp.to_list(), data.DMQuatY.to_list(), label='Y')
    plt.plot(data.TimeStamp.to_list(), data.DMQuatZ.to_list(), label='Z')
    plt.plot(data.TimeStamp.to_list(), data.DMQuatW.to_list(), label='W')
    plt.xlabel('Time [s]')
    plt.ylabel('Quaternion')
    plt.legend()

    # Attitude
    plt.figure(data_name + ' - Attitude')
    plt.plot(data.TimeStamp.to_list(), [x * 180 / pi for x in data.DMRoll.to_list()], label='Roll')
    plt.plot(data.TimeStamp.to_list(), [x * 180 / pi for x in data.DMPitch.to_list()], label='Pitch')
    plt.plot(data.TimeStamp.to_list(), [x * 180 / pi for x in data.DMYaw.to_list()], label='Yaw')
    plt.xlabel('Time [s]')
    plt.ylabel('Attitude')
    plt.legend()

def main():

    # Select the csv file to plot data with.
    file_type = select_file_type()

    if file_type == 'Exercise':
        exercise, motion_type = select_motion_type()
        if (motion_type == 'Test'):
            test = select_test(exercise)
            filepath = f'../Exercises/{exercise}/Raw Data/{motion_type}/{exercise}-Test-{test}-0.csv'
        else:
            filepath = f'../Exercises/{exercise}/Raw Data/{motion_type}/{exercise}-{motion_type}-0.csv'
    elif file_type == 'Motion Test':
        motion_test = select_motion_test()
        filepath = f'../Motion Tests/{motion_test}'

    # The amount of data to be plotted, either the first 10 seconds of the recording or the
    # entire recording.
    length = select_length()

    num_lines = pd.read_csv(filepath).shape[0]

    # Read motion data.
    data = pd.read_csv(filepath, nrows = 400 if length == 'First 10 seconds' else num_lines)

    # Adjust the timestamps so they start from 0.
    first_time_point = data.TimeStamp[0]
    for i in range(0, data.TimeStamp.shape[0]):
        data.TimeStamp[i] = data.TimeStamp[i] - first_time_point

    # Displays all data in graphs.
    if file_type == 'Exercise':
        display_data(data, f'{exercise} - {motion_type} - {length}')
    elif file_type == 'Motion Test':
        display_data(data, f'Motion Test - {motion_test}')

    plt.show()

if __name__ == '__main__':
    main()
