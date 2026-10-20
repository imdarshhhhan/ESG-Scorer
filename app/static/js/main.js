import { initComboBox } from "./comboBox.js";
import { initTabs } from "./tabs.js";
import { initCompare } from "./compare.js";
import { initSector } from "./sector.js";
import { renderCharts } from "./charts.js";

document.querySelectorAll(".combo").forEach(initComboBox);

initTabs();
initCompare();
initSector();

// draw any chart that is already on the page and visible
renderCharts(document);
