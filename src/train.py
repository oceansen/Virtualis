#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Train deep learning model to estimate power from breathing data.


Author:
    Erik Johannes Husom

Created:
    2020-09-16

"""
import sys
import time

import matplotlib.pyplot as plt
import numpy as np
import yaml

from config import MODELS_PATH, MODELS_FILE_PATH, TRAININGLOSS_PLOT_PATH
from model import *  # from model import cnn


def train(filepath):
    """Train model to estimate power.

    Args:
        filepath (str): Path to training set.

    """

    MODELS_PATH.mkdir(parents=True, exist_ok=True)

    # Load parameters
    params = yaml.safe_load(open("params.yaml"))["train"]
    net = params["net"]

    # Load training set
    train = np.load(filepath)

    X_train = train["X"]
    y_train = train["y"]

    hist_size = X_train.shape[-2]
    n_features = X_train.shape[-1]

    # Build model
    if net == "cnn":
        model = cnn(hist_size, n_features,
                    kernel_size=params["kernel_size"]
                    )
    elif net == "dnn":
        pass
    elif net == "lstm":
        model = lstm(hist_size, n_features)
    elif net == "cnndnn":
        pass

    print(model.summary())

    history = model.fit(
        X_train, y_train,
        epochs=params["n_epochs"],
        batch_size=params["batch_size"],
        validation_split=0.2
    )

    time_id = time.strftime("%Y%m%d%H%M%S")

    # model.save(MODELS_PATH / (time_id + ".h5"))
    model.save(MODELS_FILE_PATH)

    TRAININGLOSS_PLOT_PATH.parent.mkdir(parents=True, exist_ok=True)

    loss = history.history['loss']
    val_loss = history.history['val_loss']

    n_epochs = range(len(loss))

    plt.figure()
    plt.plot(n_epochs, loss, label="Training loss")
    plt.plot(n_epochs, val_loss, label="Validation loss")
    plt.legend()
    plt.savefig(TRAININGLOSS_PLOT_PATH)
    plt.show()


if __name__ == "__main__":

    np.random.seed(2020)

    train(sys.argv[1])
