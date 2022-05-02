# Exercise-Data-Processing
 
This repository is responsible for developing the exercise classification and form analysis models. The following files in the 'Model Creation' folder are run to create a model from raw motion data:

1. extract_features.py

- Splits the recorded data into overlapping motion windows. Features are extracted from each of these windows where each window is compressed into a single row in the training and testing data.

2. create_model.py

- Creates and tests a classification model using the training and testing data generated in the previous file.

## Testing Models

To test a model without overwriting the model files that are used in the project, you can run 'test_model.py' within the 'Tools' folder. This file allows you to pick a temporary model to create from a selection of exercises, or an exercise classifier by selecting 'Exercise'. The temporary model is then tested against unseen data, displaying a classification report and confusion matrix (which should match the confusion matrices shown in the final report document).
