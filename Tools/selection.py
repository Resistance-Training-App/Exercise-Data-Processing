import glob, inquirer

def select_file_type():
    """
    Select the type of file, either an exercise training recording session or a motion test used
    for debugging.
    """

    choices = ['Exercise', 'Motion Test']

    question = [inquirer.List('file_type',
                message='Pick a type of motion to extract from a CSV file',
                choices=choices)]

    # Prompt the user to select an exercise.
    file_type = inquirer.prompt(question)['file_type']

    return file_type

def select_motion_test():
    """Select a specific motion test."""

    choices = []

    # Iterate though all motion tests and store their names in a list.
    for filepath in glob.iglob('../Motion Tests/**', recursive=False):
        motion_test = filepath.split('/')[-1]
        choices.append(motion_test)

    question = [inquirer.List('motion_test',
                message='Pick a motion test',
                choices=choices)]

    # Prompt the user to select an motion test.
    motion_test = inquirer.prompt(question)['motion_test']

    return motion_test

def select_exercise():
    """Select a specific exercise."""

    choices = []

    # Iterate though all exercise folders and store their names in a list.
    for filepath in glob.iglob('../Exercises/**', recursive=False):
        exercise = filepath.split('/')[-1]
        if (exercise != 'Other'):
            choices.append(exercise)

    question = [inquirer.List('exercise',
                message='Pick an Exercise',
                choices=choices)]

    # Prompt the user to select an exercise.
    exercise = inquirer.prompt(question)['exercise']

    return exercise

def select_motion_type():
    """Select specific type of exercise form."""

    exercise = select_exercise()

    choices = []

    # Iterate though all exercise folders and store their names in a list.
    for filepath in glob.iglob(f'../Exercises/{exercise}/Raw Data/**', recursive=False):
        motion_type = filepath.split('/')[-1]
        choices.append(motion_type)

    question = [inquirer.List('motion_type',
                message='Pick a Motion Type',
                choices=choices)]

    # Prompt the user to select an exercise.
    motion_type = inquirer.prompt(question)['motion_type']

    return exercise, motion_type

def select_test(exercise):
    """Select a recording session used to test an ML model."""

    choices = []

    # Iterate though all exercise folders and store their names in a list.
    for filepath in glob.iglob(f'../Exercises/{exercise}/Raw Data/Test/**', recursive=False):
        motion_type = filepath.split('/')[-1].split('-')[-2]
        choices.append(motion_type)

    question = [inquirer.List('test',
                message='Pick a Test',
                choices=choices)]

    # Prompt the user to select an exercise.
    test = inquirer.prompt(question)['test']

    return test

def select_length():
    """
    Select the length of data to be read, either the first 10 seconds of the file or the entire
    file.
    """

    choices = ['First 10 seconds', 'All Data']

    question = [inquirer.List('length',
                message='Pick a Length to extract from the CSV file.',
                choices=choices)]

    # Prompt the user to select an exercise.
    length = inquirer.prompt(question)['length']

    return length

if __name__ == '__main__':
    select_exercise()
