import numpy as np
import matplotlib.pyplot as plt
import wfdb

def anomaly_detection(record, annotation, dissimilarity, alpha=0.185, plot=False):
    mean, std = np.mean(dissimilarity), np.std(dissimilarity)
    threshold = mean + alpha * std
    print("dissimilarity: min: {}, max: {}, mean: {}, std: {}".format(min(dissimilarity), max(dissimilarity), mean, std))
    print("threshold:", threshold)

    # anomaly determined by thresholding
    predict_label = np.ones((len(dissimilarity),))
    print(len(predict_label))
    predict_anomaly_index = np.where(dissimilarity > threshold)
    predict_label[predict_anomaly_index] = 0
    print("predicted anomaly:", len(predict_anomaly_index[0]))
    return predict_label

def test_thresh(record, annotation, dissimilarity, true_anomaly):
    performances, alpha = [],[]
    for a in range(0,30):
        predicted = anomaly_detection(record, annotation, dissimilarity, a/10)
        num_anomaly = len(true_anomaly[0])
        false_percentage = len(predicted[0]) / num_anomaly

        # specificity: true negative rate
        inters = np.intersect1d(predicted, true_anomaly)
        spec = len(inters) / num_anomaly

        # maximize the performance
        performance = 2 * false_percentage * spec / (false_percentage + spec)

        # false alarm rate:
        #FAR = (predicted.shape[0] - len(inters)) / num_anomaly

        performances.append(performance)
        alpha.append(a/10)


    plt.figure()
    plt.plot(alpha, performances)
    plt.show()



