import pandas as pd

def create_train_test_split(motion_types):
    """Splits the data into a train test split of 80% to 20% respectively."""

    print('Creating training and testing data.')

    # Create empty train and test data frames.
    train = pd.DataFrame()
    test = pd.DataFrame()
    all_data = pd.DataFrame()

    # Iterate through each type of motion adding a proportion of the data to training and testing.
    for motion in motion_types.values():
        train = train.append(motion[0:int(len(motion)*0.8)], ignore_index=True)
        test = test.append(motion[int(len(motion)*0.8):len(motion)], ignore_index=True)
        all_data = all_data.append(motion, ignore_index=True)

    return train, test, all_data
