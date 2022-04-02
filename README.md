# Exercise-Data-Processing
 
This repository is responsible for developing the exercise classification and form analysis models. The following files in the 'Model Creation' folder are run to create a model from raw motion data:

1. extract_features.py

- Splits the recorded data into overlapping motion windows. Features are extracted from each of these windows where each window is compressed into a single row in the training and testing data.

2. create_model.py

- Creates and tests a classification model using the training and testing data generated in the previous file.
