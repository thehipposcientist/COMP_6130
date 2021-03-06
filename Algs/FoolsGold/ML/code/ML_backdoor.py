from __future__ import division
from numpy.linalg import norm
import matplotlib.pyplot as plt

import model_aggregator
import softmax_model_test
import softmax_model_obj
import poisoning_compare

import numpy as np
import utils

import pdb
import sys
np.set_printoptions(suppress=True)

# Just a simple sandbox for testing out python code, without using Go.
def debug_signal_handler(signal, frame):
    import pdb
    pdb.set_trace()


import signal
signal.signal(signal.SIGINT, debug_signal_handler)


def basic_conv(dataset, num_params, softmax_test, iterations=3000):

    batch_size = 5

    # Global
    softmax_model = softmax_model_obj.SoftMaxModel(dataset, numClasses)

    print("Start training")

    weights = np.random.rand(num_params) / 100.0

    train_progress = np.zeros(iterations)
    test_progress = np.zeros(iterations)

    for i in xrange(iterations):
        deltas = softmax_model.privateFun(weights, batch_size=batch_size)
        weights = weights + deltas

        if i % 100 == 0:
            print("Train error: %.10f" % softmax_test.train_error(weights))

    print("Done iterations!")
    print("Train error: %d", softmax_test.train_error(weights))
    print("Test error: %d", softmax_test.test_error(weights))
    return weights


def non_iid(model_names, numClasses, numParams, softmax_test, krum_clip=1, iterations=3000,
    ideal_attack=False):

    # SGD batch size
    batch_size = 50

    # The number of local steps each client takes
    fed_avg_size = 10

    list_of_models = []

    for dataset in model_names:
        list_of_models.append(softmax_model_obj.SoftMaxModel(dataset, numClasses))

    # Include the model that sends the ideal vector on each iteration
    if ideal_attack:
        list_of_models.append(softmax_model_obj.SoftMaxModelEvil(dataPath +
           "_bad_ideal_4_9", numClasses))

    numClients = len(list_of_models)
    model_aggregator.init(numClients, numParams, numClasses)

    print("Start training across " + str(numClients) + " clients.")

    weights = np.random.rand(numParams) / 100.0
    train_progress = []

    # The number of previous iterations to use FoolsGold on
    memory_size = 0
    delta_memory = np.zeros((numClients, numParams, memory_size))

    summed_deltas = np.zeros((numClients, numParams))

    for i in xrange(iterations):

        delta = np.zeros((numClients, numParams))

        ##################################
        # Use significant features filter or not
        ##################################
        
        # Significant features filter, the top k biggest weights
        # topk = int(numParams / 2)
        # sig_features_idx = np.argpartition(weights, -topk)[-topk:]
        sig_features_idx = np.arange(numParams)

        ##################################
        # Use history or not
        ##################################

        if memory_size > 0:

            for k in range(len(list_of_models)):
            
                delta[k, :] = list_of_models[k].privateFun(weights,
                   batch_size=batch_size, num_iterations=fed_avg_size)

                # normalize delta
                if np.linalg.norm(delta[k, :]) > 1:
                    delta[k, :] = delta[k, :] / np.linalg.norm(delta[k, :])

                delta_memory[k, :, i % memory_size] = delta[k, :]

            # Track the total vector from each individual client
            summed_deltas = np.sum(delta_memory, axis=2)

        else:

            for k in range(len(list_of_models)):

                delta[k, :] = list_of_models[k].privateFun(weights, 
                    batch_size=batch_size, num_iterations=fed_avg_size)

                # normalize delta
                if np.linalg.norm(delta[k, :]) > 1:
                    delta[k, :] = delta[k, :] / np.linalg.norm(delta[k, :])

            # Track the total vector from each individual client
            summed_deltas = summed_deltas + delta
        
        ##################################
        # Use FoolsGold or something else
        ##################################

        # Use Foolsgold (can optionally clip gradients via Krum)
        this_delta = model_aggregator.foolsgold(delta, summed_deltas, 
            sig_features_idx, i, weights, clip=0)
        
        # Krum
        # if krum_clip == 0:
        #     this_delta = model_aggregator.average(delta)
        # else:
        #     this_delta = model_aggregator.krum(delta, clip=krum_clip)
        
        # Simple Average
        # this_delta = model_aggregator.average(delta)

        weights = weights + this_delta

        # if i % 200 == 0:
        #     error = softmax_test.train_error(weights)
        #     print("Train error: %.10f" % error)
        #     train_progress.append(error)

    print("Done iterations!")
    # print("Train error: %d", softmax_test.train_error(weights))
    # print("Test error: %d", softmax_test.test_error(weights))
    return weights


# amazon: 50 classes, 10000 features
# mnist: 10 classes, 784 features
# kdd: 23 classes, 41 features
if __name__ == "__main__":
    argv = sys.argv[1:]

    dataset = argv[0]
    iterations = int(argv[1])

    if (dataset == "mnist"):
        numClasses = 10
        numFeatures = 784
    elif (dataset == "kddcup"):
        numClasses = 23
        numFeatures = 41
    elif (dataset == "amazon"):
        numClasses = 50
        numFeatures = 10000
    else:
        print("Dataset " + dataset + " not found. Available datasets: mnist kddcup amazon")

    numParams = numClasses * numFeatures
    dataPath = dataset + "/" + dataset

    full_model = softmax_model_obj.SoftMaxModel(dataPath + "_train", numClasses)
    Xtest, ytest = full_model.get_data()

    backdoor_model = softmax_model_obj.SoftMaxModel(dataPath + "_backdoor_test", numClasses)
    Xback, yback = backdoor_model.get_data()

    to_class = '7'

    for run in range(5):

        backdoor_eval_data = np.zeros((10, 3))
        for sybil_count in range(10):

            models = []

            for i in range(numClasses):
                # Try a little more IID
                models.append(dataPath + str(i))

            for i in range(sybil_count):
                models.append(dataPath + "_backdoor_" + to_class)

            softmax_test = softmax_model_test.SoftMaxModelTest(dataset, numClasses, numFeatures)
            
            weights = non_iid(models, numClasses, numParams, softmax_test,
                iterations=iterations, krum_clip=sybil_count, ideal_attack=False)

            score = poisoning_compare.backdoor_eval(Xback, yback, weights, int(to_class), numClasses, numFeatures)
            backdoor_eval_data[sybil_count] = score

        np.savetxt("backdoor_fgavg_" + str(run) + ".csv", backdoor_eval_data, fmt='%.5f', delimiter=',')

    # Sandbox: difference between ideal bad model and global model
    compare = False
    if compare:
        bad_weights = basic_conv(dataPath + "_bad_ideal_" + from_class + "_" +
           to_class, numParams, softmax_test)
        poisoning_compare.eval(Xtest, ytest, bad_weights, int(from_class),
            int(to_class), numClasses, numFeatures)

        diff = np.reshape(bad_weights - weights, (numClasses, numFeatures))
        abs_diff = np.reshape(np.abs(bad_weights - weights), (numClasses,
           numFeatures))
