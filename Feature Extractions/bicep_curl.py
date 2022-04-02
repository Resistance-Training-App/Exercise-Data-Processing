def bicep_curl(window):
    """Extracts the features from a single window of a bicep curl."""

    # Total number of data points in a motion window.
    total_data_points = 160

    # The name of the type of motion E.g. BadRange.
    activity = window.iloc[0]['activity']

    # Feature to detect a bicep curl with bad range.
    # Finds the difference between the largest and smallest values of Gravity-X in the motion
    # window.
    gravX_height = window['DMGrvX'].max() - window['DMGrvX'].min()

    # Feature to detect a bicep curl that is too fast.
    # Finds the maximum between the highest acceleration and highest deceleration in the motion
    # window on the X-axis
    accelX_max = max(window['DMUAccelX'].max(), abs(window['DMUAccelX'].min()))

    # Binary feature to detect when a bicep curl is occuring.
    # This is '1' if the majority of rotation Y and Z value pairs within the window are positive
    # and negative.
    rot_diff = 0
    for Y_value, Z_value in zip(window['DMRotY'].tolist(), window['DMRotZ'].tolist()):
        if ((Y_value < 0 and Z_value > 0) or (Y_value > 0 and Z_value < 0)):
            rot_diff += 1

    if rot_diff > total_data_points * 0.875:
        rot_symmetry = 1
    else:
        rot_symmetry = 0

    return {'accelX_max': accelX_max,
            'activity': activity,
            'gravX_height': gravX_height,
            'rot_symmetry': rot_symmetry}
