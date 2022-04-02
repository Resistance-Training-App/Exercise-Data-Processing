def format_df(df, filename, exercise):
    """
    Formats the data frame by adding the target column 'Activity' and removing unnecessary
    columns.
    """

    filename_array = filename.split('-')

    # Use the first word in the file name if it is general exercise classification or the motion
    # is other.
    if (exercise == 'Exercise' or filename_array[0] == 'Other'):
        form_type = filename_array[0]
    else:
        form_type = filename_array[1]

    num_rows = len(df.index)

    # Add the target column.
    activity_column = [form_type] * num_rows
    df['activity'] = activity_column

    # Remove unnecessary columns.
    df = df.drop(['SessionID', 'LoggingTime', 'UID', 'RecNo', 'Hertz', 'Activity', 'MoveType',
                  'Wrist', 'Side', 'TimeStamp', 'AccelroX', 'AceelroY', 'AceelroZ'],
                  axis=1)

    return df
