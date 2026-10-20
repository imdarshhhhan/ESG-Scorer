from app import config
from app.services.data_loader import loadDisplayData

# which css class each label should get (the styles live in static/css/cards.css)
riskClasses = {"Low Risk": "tag-low", "Medium Risk": "tag-medium", "High Risk": "tag-high"}
performanceClasses = {
    "Excellent": "tag-excel",
    "Good": "tag-good",
    "Average": "tag-avg",
    "Poor": "tag-poor",
}


def buildScoreBar(label, value, maxValue, colorClass):
    percent = min(100, round(value / maxValue * 100))
    return {"label": label, "value": value, "percent": percent, "colorClass": colorClass}


def buildSectorRank(row):
    displayDf = loadDisplayData()
    sectorName = row["sector"].strip()
    sectorCompanies = displayDf[displayDf["sector"].str.strip() == sectorName]

    totalCompanies = len(sectorCompanies)
    companiesBelow = (sectorCompanies["total_esg_score"] < row["total_esg_score"]).sum()
    percent = round(companiesBelow / totalCompanies * 100)

    if percent >= 60:
        toneClass = "tone-good"
    elif percent >= 35:
        toneClass = "tone-mid"
    else:
        toneClass = "tone-low"

    return {"percent": int(percent), "sector": row["sector"], "toneClass": toneClass}


def buildDiffText(diffValue):
    sign = "+" if diffValue >= 0 else ""
    return f"{sign}{diffValue}"


def buildCard(row, trust):
    """Turns one company row into a plain dictionary the card template can print."""
    sectorAvgDiff = float(row["sector_avg_diff"])

    return {
        "name": row["name"],
        "trust": trust,
        "marketType": row["market_type"],
        "sector": row["sector"],
        "bars": [
            buildScoreBar("Environment", int(row["environment_score"]), config.maxEnvironmentScore, "fill-env"),
            buildScoreBar("Social", int(row["social_score"]), config.maxSocialScore, "fill-social"),
            buildScoreBar("Governance", int(row["governance_score"]), config.maxGovernanceScore, "fill-gov"),
        ],
        "totalEsgScore": int(row["total_esg_score"]),
        "sectorAvgDiff": buildDiffText(sectorAvgDiff),
        "diffClass": "diff-pos" if sectorAvgDiff >= 0 else "diff-neg",
        "gradeImpact": row["grade_impact"],
        "riskLevel": row["risk_level"],
        "riskClass": riskClasses.get(row["risk_level"], "tag-medium"),
        "performanceLevel": row["performance_level"],
        "performanceClass": performanceClasses.get(row["performance_level"], "tag-avg"),
        "sectorRank": buildSectorRank(row),
    }
