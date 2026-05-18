const filterForm = document.querySelector("#preview-filter-form");
const searchInput = document.querySelector("#demo-search");
const rows = Array.from(document.querySelectorAll("#preview-table-body .preview-row"));
const resultCount = document.querySelector("#preview-result-count");
const emptyState = document.querySelector("#preview-empty");
const totalModels = document.querySelector("#demo-total-models");
const openModels = document.querySelector("#demo-open-models");
const yearCount = document.querySelector("#demo-year-count");
const benchmarkCount = document.querySelector("#demo-benchmark-count");
const timelineBars = Array.from(document.querySelectorAll("#demo-timeline span"));

function rowMatches(row, filters) {
  const year = Number(row.dataset.year);
  const topicText = row.dataset.topic || "";
  const modelText = `${row.dataset.model} ${row.dataset.paradigm} ${topicText}`.toLowerCase();

  if (filters.query && !modelText.includes(filters.query)) {
    return false;
  }

  if (filters.yearFrom && year < Number(filters.yearFrom)) {
    return false;
  }

  if (filters.yearTo && year > Number(filters.yearTo)) {
    return false;
  }

  if (filters.paradigm && row.dataset.paradigm !== filters.paradigm) {
    return false;
  }

  if (filters.topic && !topicText.includes(filters.topic)) {
    return false;
  }

  if (filters.openSource && row.dataset.openSource !== filters.openSource) {
    return false;
  }

  return true;
}

function readFilters() {
  const data = new FormData(filterForm);
  return {
    query: (searchInput.value || "").trim().toLowerCase(),
    yearFrom: data.get("yearFrom") || "",
    yearTo: data.get("yearTo") || "",
    paradigm: data.get("paradigm") || "",
    topic: data.get("topic") || "",
    openSource: data.get("openSource") || "",
  };
}

function updateTimeline(visibleRows) {
  const counts = new Map();
  visibleRows.forEach((row) => {
    counts.set(row.dataset.year, (counts.get(row.dataset.year) || 0) + 1);
  });
  const maxCount = Math.max(...counts.values(), 1);

  timelineBars.forEach((bar) => {
    const count = counts.get(bar.dataset.year) || 0;
    const height = count === 0 ? 18 : 24 + (count / maxCount) * 68;
    bar.style.height = `${height}px`;
    bar.dataset.count = count;
    bar.classList.toggle("is-empty", count === 0);
  });
}

function applyFilters() {
  const filters = readFilters();
  const visibleRows = [];

  rows.forEach((row) => {
    const visible = rowMatches(row, filters);
    row.hidden = !visible;
    if (visible) {
      visibleRows.push(row);
    }
  });

  resultCount.textContent = `(${visibleRows.length} results)`;
  emptyState.hidden = visibleRows.length !== 0;
  totalModels.textContent = visibleRows.length;
  openModels.textContent = visibleRows.filter((row) => row.dataset.openSource === "yes").length;
  yearCount.textContent = new Set(visibleRows.map((row) => row.dataset.year)).size;
  benchmarkCount.textContent = new Set(visibleRows.map((row) => row.dataset.benchmark)).size;
  updateTimeline(visibleRows);
}

if (filterForm && searchInput) {
  filterForm.addEventListener("submit", (event) => {
    event.preventDefault();
    applyFilters();
  });

  filterForm.addEventListener("reset", () => {
    window.setTimeout(applyFilters, 0);
  });

  searchInput.addEventListener("input", applyFilters);
  applyFilters();
}
