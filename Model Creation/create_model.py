import sys
import pandas as pd
import numpy as np
import coremltools as ct
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.ensemble import GradientBoostingClassifier

sys.path.append('../Tools')
from selection import *
from plot_confusion_matrix import plot_confusion_matrix

# Have to used downgraded scikit learn version in order convert the model to a .mlmodel file. This
# causes a large volume of depreciation warnings which this silences.
if not sys.warnoptions:
    import warnings
    warnings.simplefilter('ignore')
warnings.filterwarnings('ignore', category=DeprecationWarning)

def create_model(exercise, train):
    """Create and train the model and save as a .mlmodel file."""

    X_train = train.drop(['activity'], axis=1)
    Y_train = train['activity'].tolist()

    # Create model.
    model = GradientBoostingClassifier(verbose=1,
                                       random_state=0)

    # Train model.
    model.fit(X_train, Y_train)

    # Convert to a mlmodel and save as a file.
    coreml_model = ct.converters.sklearn.convert(
                        model,
                        train.drop(['activity'], axis=1).columns.tolist(),
                        'activity')

    coreml_model.save(f'../Exercises/{exercise}/{exercise}.mlmodel')

    return model

def model_metrics(exercise, test, model):
    """Evaluate the created model with a classification report and confusion matrix."""

    X_test = test.drop(['activity'], axis=1)
    Y_test = test['activity'].tolist()

    # Classification report.
    prediction = model.predict(X_test)
    print(f'\n{exercise} Model:\n')
    print(classification_report(Y_test, prediction))

    # Calculate confusion matrix.
    matrix = confusion_matrix(Y_test, prediction)

    # Plot non-normalized confusion matrix and save as an image.
    plt.figure()
    plot_confusion_matrix(matrix,
                          classes=(np.sort(test['activity'].unique())),
                          normalize=True,
                          title=f'{exercise} Confusion Matrix')

    plt.savefig(f'../Exercises/{exercise}/Metrics/Confusion Matrix.png', bbox_inches='tight')

def main():

    # Select exercise to create a model for.
    exercise = select_exercise()

    train_filepath = f'../Exercises/{exercise}/Processed Data/train.csv'
    test_filepath = f'../Exercises/{exercise}/Processed Data/test.csv'

    # Read training and testing data.
    train = pd.read_csv(train_filepath)
    test = pd.read_csv(test_filepath)

    # Create model.
    model = create_model(exercise, train)

    # Calculate model metrics.
    model_metrics(exercise, test, model)

if __name__ == '__main__':
    main()
