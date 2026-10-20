import pickle
from functools import lru_cache

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

from app import config


@lru_cache(maxsize=1)
def loadDisplayData():
    return pd.read_csv(config.displayDataPath)


def trainModel():
    """Used only when model.pkl is missing: trains a fresh model and saves it."""
    preprocessedDf = pd.read_csv(config.preprocessedDataPath)
    features = preprocessedDf[config.featureColumns]
    target = preprocessedDf[config.targetColumn]

    trainFeatures, _, trainTarget, _ = train_test_split(
        features, target, test_size=0.2, random_state=1, shuffle=True
    )

    newModel = RandomForestRegressor(random_state=42)
    newModel.fit(trainFeatures, trainTarget)

    with open(config.modelPath, "wb") as modelFile:
        pickle.dump(newModel, modelFile)
    return newModel


@lru_cache(maxsize=1)
def loadModel():
    try:
        with open(config.modelPath, "rb") as modelFile:
            return pickle.load(modelFile)
    except FileNotFoundError:
        return trainModel()
