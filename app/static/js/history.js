// Remembers the last few comparisons for this browser tab (like the old session state).

const storageKey = "esgRecentSearches";
const maxItems = 5;

function loadHistory() {
  try {
    return JSON.parse(sessionStorage.getItem(storageKey)) || [];
  } catch (error) {
    return [];
  }
}

function saveHistory(historyList) {
  try {
    sessionStorage.setItem(storageKey, JSON.stringify(historyList));
  } catch (error) {
    // storage can be blocked by the browser; history just won't be remembered
  }
}

export function initHistory({ wrap, row, onPick }) {
  function render() {
    const historyList = loadHistory();
    wrap.hidden = historyList.length === 0;
    row.replaceChildren();

    historyList.forEach(([firstName, secondName]) => {
      const button = document.createElement("button");
      button.type = "button";
      button.className = "btn";
      button.textContent = `${firstName} vs ${secondName}`;
      button.addEventListener("click", () => onPick(firstName, secondName));
      row.appendChild(button);
    });

    const clearButton = document.createElement("button");
    clearButton.type = "button";
    clearButton.className = "btn";
    clearButton.textContent = "🗑 Clear";
    clearButton.addEventListener("click", () => {
      saveHistory([]);
      render();
    });
    row.appendChild(clearButton);
  }

  function add(firstName, secondName) {
    const historyList = loadHistory();
    const alreadySaved = historyList.some(([first, second]) => first === firstName && second === secondName);
    if (!alreadySaved) historyList.unshift([firstName, secondName]);

    saveHistory(historyList.slice(0, maxItems));
    render();
  }

  render();
  return { add };
}
