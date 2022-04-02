import pandas as pd

def lateral_raise(window):
    """Extracts the features from a single window of lateral raise."""

    # The name of the type of motion E.g. BadRange.
    activity = window.iloc[0]['activity']

    # Feature to detect a lateral raise with bad range.
    # Finds the difference between the largest and smallest values of Gravity-X and Gravity-Z in
    # the motion window and adds them together.
    gravX_height = window['DMGrvX'].max() - window['DMGrvX'].min()

    # Roll height
    roll_height = abs(window['DMRoll']).max() - abs(window['DMRoll']).min()

    # Feature to detect a lateral raise that is too fast.
    # Finds the maximum between the highest rotation rate in both positive and negative directions
    # in the motion window on the Y-axis
    rotY_max = max(window['DMRotY'].max(), abs(window['DMRotY'].min()))

    avgGravX = pd.Series(window['DMGrvX'].tolist()).rolling(5).mean()
    avgGravZ = pd.Series(window['DMGrvZ'].tolist()).rolling(5).mean()
    avgRoll = pd.Series(window['DMRoll'].tolist()).rolling(5).mean()

    gravXTP = 0
    gravZTP = 0
    gravRollTP = 0

    # Counts the number of turning points for Gravity X, Z and Roll.
    for i in range(1, len(avgGravX) - 1):

        point_1 = avgGravX[i-1]
        point_2 = avgGravX[i]
        point_3 = avgGravX[i+1]

        if (point_1 < point_2 and point_3 < point_2) or ((point_1 > point_2 and point_3 > point_2)):
            gravXTP += 1

        point_1 = avgGravZ[i-1]
        point_2 = avgGravZ[i]
        point_3 = avgGravZ[i+1]

        if (point_1 < point_2 and point_3 < point_2) or ((point_1 > point_2 and point_3 > point_2)):
            gravZTP += 1

        point_1 = avgRoll[i-1]
        point_2 = avgRoll[i]
        point_3 = avgRoll[i+1]

        if (point_1 < point_2 and point_3 < point_2) or ((point_1 > point_2 and point_3 > point_2)):
            gravRollTP += 1

    # The minimum roll value captured during the motion window.
    roll_min = window['DMRoll'].min()

    return {'activity': activity,
            'gravX_height': gravX_height,
            'roll_height': roll_height,
            'roll_min': roll_min,
            'rotY_max': rotY_max,
            'TP_sum': (gravXTP + gravZTP + gravRollTP) / 10}
