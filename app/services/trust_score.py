from functools import lru_cache

import pandas as pd

from app import config
from app.services.data_loader import loadDisplayData, loadModel


def predictTrustForFrame(featureFrame):
    """Runs the model on every row and turns each prediction into a 0-100 trust score."""
    model = loadModel()
    predictions = model.predict(featureFrame[config.featureColumns])

    trustScores = []
    for prediction in predictions:
        trust = (prediction - config.rawScoreMin) / (config.rawScoreMax - config.rawScoreMin) * 100

        if trust >= 80:
            trust = trust * (1 - 0.05)
        elif trust >= 40:
            trust = trust * (1 + 0.04)
        else:
            trust = trust * (1 + 0.10)

        trustScores.append(round(max(0.0, min(100.0, float(trust))), 1))
    return trustScores


def predictTrust(environmentScore, socialScore, governanceScore):
    featureFrame = pd.DataFrame(
        [[environmentScore, socialScore, governanceScore]],
        columns=config.featureColumns,
    )
    return predictTrustForFrame(featureFrame)[0]


@lru_cache(maxsize=1)
def getAllCompaniesWithTrust():
    """Every company with its trust score, calculated once and kept in memory."""
    allDf = loadDisplayData().copy()
    allDf["trust_score"] = predictTrustForFrame(allDf)
    return allDf
