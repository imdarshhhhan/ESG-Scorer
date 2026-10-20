import plotly.graph_objects as go

from app import config


def figureToJson(figure):
    return figure.to_json().replace("<", "\\u003c")


def buildComparisonFigure(firstRow, secondRow, firstTrust, secondTrust):
    xLabels = ["Environment", "Social", "Governance", "Trust Score"]
    lines = [
        (firstRow, firstTrust, "#4A7DFF"),
        (secondRow, secondTrust, "#34D399"),
    ]

    figure = go.Figure()
    for row, trust, lineColor in lines:
        values = [
            int(row["environment_score"]),
            int(row["social_score"]),
            int(row["governance_score"]),
            trust,
        ]
        figure.add_trace(go.Scatter(
            x=xLabels,
            y=values,
            mode="lines+markers+text",
            name=row["name"],
            line=dict(color=lineColor, width=3),
            marker=dict(size=9, color=lineColor),
            text=[str(value) for value in values],
            textposition="top center",
            textfont=dict(color="#C8D8F8", size=11),
        ))

    figure.update_layout(
        title=dict(text="ESG Score Comparison",
                   font=dict(color="#E8F0FE", size=13, family="DM Serif Display")),
        xaxis=dict(color="#7B93C4", tickfont=dict(color="#C8D8F8", size=12), gridcolor="#1A2845"),
        yaxis=dict(title="Score", color="#7B93C4",
                   tickfont=dict(color="#7B93C4", size=11), gridcolor="#1A2845"),
        paper_bgcolor="#070C1A",
        plot_bgcolor="#070C1A",
        font=dict(family="DM Sans", color="#C8D8F8"),
        legend=dict(bgcolor="#0D1526", bordercolor="#1A2845",
                    borderwidth=1, font=dict(color="#C8D8F8", size=12)),
        margin=dict(t=50, b=20, l=20, r=20),
        height=380,
    )
    return figure


def buildSectorFigure(sectorDf, sectorName, avgTrust):
    topCompanies = sectorDf.head(config.topCompaniesLimit)
    totalShown = len(topCompanies)
    trustValues = topCompanies["trust_score"].tolist()
    barColors = ["#4A7DFF" if score >= avgTrust else "#F87171" for score in trustValues]

    figure = go.Figure(go.Bar(
        x=trustValues,
        y=topCompanies["name"].tolist(),
        orientation="h",
        marker_color=barColors,
        text=[f"{score}" for score in trustValues],
        textposition="outside",
        textfont=dict(color="#C8D8F8", size=11),
    ))

    figure.add_vline(
        x=avgTrust, line_dash="dash", line_color="#FBBF24", line_width=1.5,
        annotation_text=f"Sector avg {avgTrust}",
        annotation_font_color="#FBBF24", annotation_font_size=11,
    )

    figure.update_layout(
        title=dict(text=f"Top {totalShown} Companies — {sectorName}",
                   font=dict(color="#E8F0FE", size=14, family="DM Serif Display")),
        xaxis=dict(range=[0, 105], color="#5A7099", gridcolor="#1A2845",
                   tickfont=dict(color="#7B93C4")),
        yaxis=dict(autorange="reversed", color="#C8D8F8", automargin=True,
                   tickfont=dict(color="#C8D8F8", size=11)),
        paper_bgcolor="#070C1A",
        plot_bgcolor="#070C1A",
        font=dict(family="DM Sans", color="#C8D8F8"),
        margin=dict(l=20, r=60, t=50, b=20),
        height=max(350, totalShown * 38),
    )
    return figure
