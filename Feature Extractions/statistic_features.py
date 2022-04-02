import numpy as np
from scipy.signal import find_peaks
from scipy import stats

def statistic_features(data, dimension, features, fft):
    """Extracts general statistic features from a list of data."""

    isFFT = True if len(fft) > 0 else False

    # Mean
    features[f'{dimension}_mean{fft}'] = data.mean()

    # Standard deviation
    features[f'{dimension}_std{fft}'] = data.std()

    # Average absolute difference
    features[f'{dimension}_aad{fft}'] = np.mean(np.absolute(data - np.mean(data)))

    # Minimum value
    features[f'{dimension}_min{fft}'] = data.min()

    # Maximum value
    features[f'{dimension}_max{fft}'] = data.max()

    # Minimum-maximum difference 
    features[f'{dimension}_maxmin_diff{fft}'] = \
    features[f'{dimension}_max{fft}'] - features[f'{dimension}_min{fft}']

    # Median
    features[f'{dimension}_median{fft}'] = np.median(data)

    # Median absolute deviation
    features[f'{dimension}_mad{fft}'] = np.median(np.absolute(data - np.median(data)))

    # Interquartile range
    features[f'{dimension}_IQR{fft}'] = np.percentile(data, 75) - np.percentile(data, 25)

    # Number of values above the mean
    features[f'{dimension}_above_mean{fft}'] = np.sum(data > data.mean())

    # Number of local maxima
    features[f'{dimension}_peak_count{fft}'] = len(find_peaks(data)[0])

    # Skewness
    features[f'{dimension}_skewness{fft}'] = stats.skew(data)

    # Kurtosis
    features[f'{dimension}_kurtosis{fft}'] = stats.kurtosis(data)

    # Energy
    features[f'{dimension}_energy{fft}'] = np.sum(data**2) / (50 if isFFT else 100)

    if (not isFFT):

        # Number of positive values
        features[f'{dimension}_pos_count'] = np.sum(data > 0)

        # Number of negative values
        features[f'{dimension}_neg_count'] = np.sum(data < 0)
