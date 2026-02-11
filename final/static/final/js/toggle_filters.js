function toggleFilters(open = true) {
  const sidebar = document.getElementById("filterSidebar");
  const overlay = document.getElementById("filterSidebarOverlay");

  if (!sidebar || !overlay) return;

  if (open) {
    sidebar.classList.add("open");
    overlay.classList.add("active");
  } else {
    sidebar.classList.remove("open");
    overlay.classList.remove("active");
  }
}

/* Close on overlay click */
//document
//  .getElementById("filterSidebarOverlay")
//  ?.addEventListener("click", () => toggleFilters(false));

/* =========================
   ACCORDION SECTIONS
========================= */

function toggleSection(btn) {
  const content = btn.nextElementSibling;
  if (!content) return;

  content.classList.toggle("open");
}

/* =========================
   CHIP HANDLING
========================= */

const chipsContainer = document.getElementById("chipsContainer");

function updateChips() {
  if (!chipsContainer) return;

  chipsContainer.innerHTML = "";

  /* Selects */
  document.querySelectorAll("#filterSidebar select").forEach(select => {
    if (!select.name) return;

    const label = prettifyName(select.name);

    if (select.multiple) {
      Array.from(select.selectedOptions).forEach(opt => {
        addChip(select.name, opt.value, `${label}: ${opt.text}`);
      });
    } else if (select.value) {
      const text = select.options[select.selectedIndex]?.text || select.value;
      addChip(select.name, select.value, `${label}: ${text}`);
    }
  });

  /* Inputs */
  document
    .querySelectorAll("#filterSidebar input[type='text'], #filterSidebar input[type='date']")
    .forEach(input => {
      if (!input.name || !input.value) return;
      addChip(input.name, input.value, `${prettifyName(input.name)}: ${input.value}`);
    });

  chipsContainer.style.display =
    chipsContainer.children.length ? "flex" : "none";
}

/* Create chip */
function addChip(name, value, label) {
  const chip = document.createElement("div");
  chip.className = "chip";
  chip.dataset.name = name;
  chip.dataset.value = value;

  chip.innerHTML = `
    ${label}
    <button type="button" aria-label="Remove filter">&times;</button>
  `;

  chip.querySelector("button").onclick = () => removeChip(name, value);
  chipsContainer.appendChild(chip);
}

/* Remove chip + update fields */
function removeChip(name, value) {
  const field = document.querySelector(`#filterSidebar [name="${name}"]`);
  if (!field) return;

  if (field.multiple) {
    Array.from(field.options).forEach(opt => {
      if (opt.value === value) opt.selected = false;
    });
  } else {
    field.value = "";
  }

  updateChips();
}

/* Helper */
function prettifyName(name) {
  return name
    .replace(/_/g, " ")
    .replace(/\b\w/g, c => c.toUpperCase());
}

/* Build chips on load (GET filters) */
document.addEventListener("DOMContentLoaded", updateChips);




function toggleMode(mode) {
  const quick = mode === "quick";

  document.getElementById("quickRange").disabled = !quick;
  document.getElementById("fromDate").disabled = quick;
  document.getElementById("toDate").disabled = quick;
}

