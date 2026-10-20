import { renderCharts } from "./charts.js";

export function initTabs() {
  const tabButtons = document.querySelectorAll(".tab-button");
  const tabPanels = document.querySelectorAll(".tab-panel");

  tabButtons.forEach((button) => {
    button.addEventListener("click", () => {
      tabButtons.forEach((other) => other.classList.toggle("is-active", other === button));

      tabPanels.forEach((panel) => {
        const isSelected = panel.id === button.dataset.tab;
        panel.hidden = !isSelected;
        if (isSelected) renderCharts(panel);
      });
    });
  });
}
