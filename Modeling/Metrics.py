import numpy as np


def calculate_metrics(predicted, true_labels):
    """
    Input: predicted - numpy array of 0s and 1s (0 is normal)
           true_labels - numpy array of strings (beat labels from ECGData)
    Output: accuracy, sensitivity, and positive predictivity
    """
    predicted = np.array(predicted)
    binary_true_labels = (true_labels != 'N').astype(float)
    assert predicted.shape == binary_true_labels.shape

    N_beats = predicted.shape[0]
    N_correct = np.sum(predicted == binary_true_labels)
    accuracy = 100. * N_correct / N_beats
    # print(N_beats, N_correct)

    true_positive = np.sum(np.multiply(predicted, binary_true_labels))
    # print(true_positive)
    false_positive = np.sum(predicted) - true_positive
    # print(false_positive)
    false_negative = np.sum(binary_true_labels) - true_positive
    # print(false_negative)

    if true_positive + false_negative != 0:
        sensitivity = true_positive / (true_positive + false_negative)
    else:
        sensitivity = None
        print("WARNING: true_positive + false_negative == 0")

    if true_positive + false_positive != 0:
        positive_predictivity = true_positive / (true_positive + false_positive)
    else:
        positive_predictivity = None
        print("WARNING: true_positive + false_positive == 0")

    return accuracy, sensitivity, positive_predictivity
