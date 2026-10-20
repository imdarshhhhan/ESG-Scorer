from app.services.chart_service import buildSectorFigure, figureToJson
from app.services.trust_score import getAllCompaniesWithTrust

medalClasses = {1: "gold", 2: "silver", 3: "bronze"}


def getSectorNames():
    allDf = getAllCompaniesWithTrust()
    return sorted(allDf["sector"].str.strip().unique().tolist())


def buildRankRows(sectorDf, avgTrust, maxTrust):
    rankRows = []
    for index, row in sectorDf.iterrows():
        rank = index + 1
        trust = float(row["trust_score"])
        aboveAverage = round(trust - avgTrust, 1)
        sign = "+" if aboveAverage >= 0 else ""

        rankRows.append({
            "rank": rank,
            "medalClass": medalClasses.get(rank, ""),
            "name": row["name"],
            "trust": trust,
            "barPercent": round(trust / maxTrust * 100),
            "barClass": "fill-good" if trust >= avgTrust else "fill-bad",
            "diffText": f"{sign}{aboveAverage}",
            "diffClass": "diff-pos" if aboveAverage >= 0 else "diff-neg",
        })
    return rankRows


def buildSectorView(sectorName):
    """Stats, ranked rows and chart for one sector. Returns None if the sector has no companies."""
    allDf = getAllCompaniesWithTrust()
    sectorDf = (
        allDf[allDf["sector"].str.strip() == sectorName]
        .sort_values("trust_score", ascending=False)
        .reset_index(drop=True)
    )
    if sectorDf.empty:
        return None

    avgTrust = round(float(sectorDf["trust_score"].mean()), 1)
    maxTrust = float(sectorDf["trust_score"].max())
    figure = buildSectorFigure(sectorDf, sectorName, avgTrust)

    return {
        "sectorName": sectorName,
        "totalCompanies": len(sectorDf),
        "avgTrust": avgTrust,
        "topTrust": round(float(sectorDf["trust_score"].iloc[0]), 1),
        "lowTrust": round(float(sectorDf["trust_score"].iloc[-1]), 1),
        "rankRows": buildRankRows(sectorDf, avgTrust, maxTrust),
        "chartJson": figureToJson(figure),
    }
