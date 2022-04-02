import numpy as np
from statistic_features import statistic_features

def shoulder_press(window):
    """Extracts the features from a single window of shoulder press."""

    dimensions = ['x', 'y', 'z']
    features = {}

    # The name of the type of motion E.g. BadRange.
    features['activity'] = window.iloc[0]['activity']

    # Converting the signals from time domain to frequency domain using FFT.
    fft = {}
    fft['x'] = np.abs(np.fft.fft(window['DMUAccelX']))[1:51]
    fft['y'] = np.abs(np.fft.fft(window['DMUAccelY']))[1:51]
    fft['z'] = np.abs(np.fft.fft(window['DMUAccelZ']))[1:51]

    # Extract general statistic features from the x, y and z dimensions.
    for dimension in dimensions:
        statistic_features(data=window[f'DMUAccel{dimension.capitalize()}'],
                           dimension=dimension,
                           features=features,
                           fft='')

    # Average resultant acceleration
    features['avg_result_accl'] = ((window['DMUAccelX']**2 + window['DMUAccelY']**2 + window['DMUAccelZ']**2)**0.5).mean()

    # Signal magnitude area
    features['sma'] = np.sum(abs(window['DMUAccelX'])/100) + \
                      np.sum(abs(window['DMUAccelY'])/100) + \
                      np.sum(abs(window['DMUAccelZ'])/100)

    # Extract general statistic features from the fft x, y and z dimensions.
    for dimension in dimensions:
        statistic_features(data=fft[dimension],
                           dimension=dimension,
                           features=features,
                           fft='_fft')

    # Average resultant acceleration
    features['avg_result_accl_fft'] = ((fft['x']**2 + fft['y']**2 + fft['z']**2)**0.5).mean()

    # Signal magnitude area
    features['sma_fft'] = np.sum(abs(fft['x'])/50) + \
                          np.sum(abs(fft['y'])/50) + \
                          np.sum(abs(fft['z'])/50)

    # Sort the features alphabetically.
    sorted_features = {key: value for key, value in sorted(features.items())}

    return sorted_features
