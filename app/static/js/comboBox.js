// A searchable dropdown. Type to filter, click or press Enter to pick.
// Fires a "combochange" event on the root element when the value changes.

export function initComboBox(root) {
  const input = root.querySelector(".combo-input");
  const list = root.querySelector(".combo-list");
  const emptyNote = list.querySelector(".combo-empty");
  const items = Array.from(list.querySelectorAll("li[data-value]"));
  const placeholderText = root.dataset.placeholder || "";

  let selectedValue = root.dataset.value || "";
  let activeItem = null;

  function showSelectedValue() {
    input.value = selectedValue;
    input.placeholder = placeholderText;
  }

  function getVisibleItems() {
    return items.filter((item) => !item.hidden);
  }

  function setActiveItem(item) {
    if (activeItem) activeItem.classList.remove("is-active");
    activeItem = item;
    if (!item) return;

    item.classList.add("is-active");
    const itemTop = item.offsetTop;
    const itemBottom = itemTop + item.offsetHeight;
    if (itemTop < list.scrollTop) list.scrollTop = itemTop;
    else if (itemBottom > list.scrollTop + list.clientHeight) list.scrollTop = itemBottom - list.clientHeight;
  }

  function filterItems(searchText) {
    const text = searchText.trim().toLowerCase();
    items.forEach((item) => {
      item.hidden = !item.dataset.value.toLowerCase().includes(text);
    });
    emptyNote.hidden = getVisibleItems().length > 0;
  }

  function openList() {
    filterItems("");
    items.forEach((item) => item.classList.toggle("is-selected", item.dataset.value === selectedValue));
    list.hidden = false;
    input.setAttribute("aria-expanded", "true");

    const selectedItem = items.find((item) => item.dataset.value === selectedValue);
    list.scrollTop = selectedItem ? Math.max(0, selectedItem.offsetTop - 80) : 0;
    setActiveItem(null);
  }

  function closeList() {
    list.hidden = true;
    input.setAttribute("aria-expanded", "false");
    setActiveItem(null);
  }

  function pickValue(value) {
    const hasChanged = value !== selectedValue;
    selectedValue = value;
    showSelectedValue();
    closeList();
    input.blur();
    if (hasChanged) {
      root.dispatchEvent(new CustomEvent("combochange", { detail: { value }, bubbles: true }));
    }
  }

  function moveActiveItem(step) {
    const visibleItems = getVisibleItems();
    if (visibleItems.length === 0) return;
    const currentIndex = visibleItems.indexOf(activeItem);
    const nextIndex = (currentIndex + step + visibleItems.length) % visibleItems.length;
    setActiveItem(visibleItems[nextIndex]);
  }

  input.addEventListener("focus", () => {
    openList();
    input.select();
  });

  input.addEventListener("click", () => {
    if (list.hidden) openList();
  });

  input.addEventListener("input", () => {
    list.hidden = false;
    filterItems(input.value);
    setActiveItem(getVisibleItems()[0] || null);
  });

  input.addEventListener("keydown", (event) => {
    if (event.key === "ArrowDown") {
      event.preventDefault();
      if (list.hidden) openList();
      moveActiveItem(1);
    } else if (event.key === "ArrowUp") {
      event.preventDefault();
      moveActiveItem(-1);
    } else if (event.key === "Enter") {
      event.preventDefault();
      if (activeItem) pickValue(activeItem.dataset.value);
    } else if (event.key === "Escape") {
      showSelectedValue();
      closeList();
    }
  });

  input.addEventListener("blur", () => {
    closeList();
    showSelectedValue();
  });

  // mousedown (not click) so the input does not lose focus before we read the choice
  list.addEventListener("mousedown", (event) => {
    event.preventDefault();
    const item = event.target.closest("li[data-value]");
    if (item) pickValue(item.dataset.value);
  });

  root.getValue = () => selectedValue;
  root.setValue = (value) => {
    selectedValue = value;
    showSelectedValue();
  };

  showSelectedValue();
}
