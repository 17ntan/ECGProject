import numpy as np
import matplotlib.pyplot as plt
import wfdb

def anomaly_detection(record, annotation, dissimilarity, alpha=0.6, plot=False):
    dissimilarity = dissimilarity[1:] # dissimilarity of first beat is super large(1495.7, others:4 to 17?)
    mean, std = np.mean(dissimilarity), np.std(dissimilarity)
    threshold = mean + alpha * std
    #print("mean:", mean, "std:", std, "threshold:", threshold)

    # anomaly determined by thresholding
    predict_anomaly = np.where(dissimilarity > threshold)
    #print("predicted label index:", predict_anomaly)

    if plot:
        wfdb.plot_wfdb(record=record, annotation=annotation, title='Record 100 from MIT-BIH Arrhythmia Database')

    return predict_anomaly

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



