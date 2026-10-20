// Finds every chart placeholder inside a container and draws it with Plotly.
// The figure itself is built on the server and sent as JSON right after the placeholder.

const plotConfig = { responsive: true, displaylogo: false };

export function renderCharts(container) {
  container.querySelectorAll("[data-chart]").forEach((chartBox) => {
    if (chartBox.offsetParent === null) return; // hidden tab: draw it when it becomes visible

    if (chartBox.dataset.drawn === "true") {
      Plotly.Plots.resize(chartBox);
      return;
    }

    const dataTag = chartBox.nextElementSibling;
    const figure = JSON.parse(dataTag.textContent);
    Plotly.newPlot(chartBox, figure.data, figure.layout, plotConfig);
    chartBox.dataset.drawn = "true";
  });
}
