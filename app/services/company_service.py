from app.services.card_builder import buildCard
from app.services.chart_service import buildComparisonFigure, figureToJson
from app.services.data_loader import loadDisplayData
from app.services.trust_score import predictTrust


def getCompanyNames():
    return sorted(loadDisplayData()["name"].tolist())


def findCompany(companyName):
    displayDf = loadDisplayData()
    matches = displayDf[displayDf["name"] == companyName]
    return matches.iloc[0] if not matches.empty else None


def getRowTrust(row):
    return predictTrust(row["environment_score"], row["social_score"], row["governance_score"])


def buildWinnerBanner(firstRow, secondRow, firstTrust, secondTrust):
    if firstTrust == secondTrust:
        return {"isTie": True}

    firstWins = firstTrust > secondTrust
    winnerScore = max(firstTrust, secondTrust)
    loserScore = min(firstTrust, secondTrust)

    return {
        "isTie": False,
        "winnerName": firstRow["name"] if firstWins else secondRow["name"],
        "loserName": secondRow["name"] if firstWins else firstRow["name"],
        "winnerScore": winnerScore,
        "loserScore": loserScore,
        "gap": round(winnerScore - loserScore, 1),
    }


def buildComparison(firstName, secondName):
    """Everything the compare results template needs. Returns None if a name is unknown."""
    firstRow = findCompany(firstName)
    secondRow = findCompany(secondName)
    if firstRow is None or secondRow is None:
        return None

    firstTrust = getRowTrust(firstRow)
    secondTrust = getRowTrust(secondRow)
    figure = buildComparisonFigure(firstRow, secondRow, firstTrust, secondTrust)

    return {
        "cards": [buildCard(firstRow, firstTrust), buildCard(secondRow, secondTrust)],
        "banner": buildWinnerBanner(firstRow, secondRow, firstTrust, secondTrust),
        "chartJson": figureToJson(figure),
    }
