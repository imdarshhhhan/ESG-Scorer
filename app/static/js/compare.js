import { renderCharts } from "./charts.js";
import { initHistory } from "./history.js";

export function initCompare() {
  const firstBox = document.getElementById("companyOne");
  const secondBox = document.getElementById("companyTwo");
  const compareButton = document.getElementById("compareButton");
  const resultsBox = document.getElementById("compareResults");

  // clicking a recent search only fills the two dropdowns, like before
  const history = initHistory({
    wrap: document.getElementById("historyWrap"),
    row: document.getElementById("historyRow"),
    onPick(firstName, secondName) {
      firstBox.setValue(firstName);
      secondBox.setValue(secondName);
      resultsBox.innerHTML = "";
    },
  });

  compareButton.addEventListener("click", async () => {
    const firstName = firstBox.getValue();
    const secondName = secondBox.getValue();
    const query = new URLSearchParams({ company1: firstName, company2: secondName });

    compareButton.disabled = true;
    try {
      const response = await fetch(`/compare?${query}`);
      resultsBox.innerHTML = await response.text();

      if (response.ok) {
        history.add(firstName, secondName);
        renderCharts(resultsBox);
      }
    } catch (error) {
      resultsBox.innerHTML = '<div class="alert">Something went wrong. Please try again.</div>';
    } finally {
      compareButton.disabled = false;
    }
  });
}
