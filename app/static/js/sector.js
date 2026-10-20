import { renderCharts } from "./charts.js";

export function initSector() {
  const sectorBox = document.getElementById("sectorSelect");
  const resultsBox = document.getElementById("sectorResults");

  sectorBox.addEventListener("combochange", async (event) => {
    const query = new URLSearchParams({ name: event.detail.value });

    try {
      const response = await fetch(`/sector?${query}`);
      resultsBox.innerHTML = await response.text();
      renderCharts(resultsBox);
    } catch (error) {
      resultsBox.innerHTML = '<div class="alert">Something went wrong. Please try again.</div>';
    }
  });
}
