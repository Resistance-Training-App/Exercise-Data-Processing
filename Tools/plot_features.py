import pandas as pd
import matplotlib.pyplot as plt
from selection import select_exercise

def plot_features():
    """Plots the average feature value of all features for all training and testing data."""

    # Pick an exercise to create the model for.
    exercise = select_exercise()

    # Read the whole dataset of extracted features.
    df = pd.read_csv(f'../Exercises/{exercise}/Processed Data/all.csv')

    feature_names = []
    motion_types = []
    average_series = []

    # Find the mean of each column seperated by motion type.
    for name, _ in df.iteritems():
        try:
            average_series.append(df.groupby('activity')[name].mean())
        except:
            pass

    # Create separate lists of feature names and motion types.
    for column in average_series:
        feature_names.append(column.name)
        for axis in column.axes[0]:
            motion_types.append(axis) if axis not in motion_types else motion_types

    chart_data = pd.DataFrame(columns=feature_names)

    # Add each feature to the chart_data dataframe.
    for feature in average_series:
        values = []
        for motion_type in motion_types:
            values.append(feature[motion_type])
        chart_data[feature.name] = values

    chart_data['activity'] = motion_types

    # plot grouped bar chart.
    chart_data.plot(x='activity',
                    kind='bar',
                    stacked=False,
                    title='Feature values for each type of motion')
    plt.autoscale()
    plt.show()

if __name__ == '__main__':
    plot_features()
