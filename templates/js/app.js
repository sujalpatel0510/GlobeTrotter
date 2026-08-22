// GlobeTrotter — shared front-end interactions (no backend, UI only)

document.addEventListener('DOMContentLoaded', () => {

  // Mobile nav toggle
  const toggle = document.querySelector('.nav-toggle');
  const links = document.querySelector('.nav-links');
  if (toggle && links) {
    toggle.addEventListener('click', () => {
      links.classList.toggle('open');
    });
  }

  // Generic tab switcher: elements with [data-tabs] wrapping [data-tab] buttons
  // and sibling panels with [data-tab-panel]
  document.querySelectorAll('[data-tabs]').forEach((group) => {
    const buttons = group.querySelectorAll('[data-tab]');
    buttons.forEach((btn) => {
      btn.addEventListener('click', () => {
        buttons.forEach((b) => b.classList.remove('active'));
        btn.classList.add('active');
        const target = btn.getAttribute('data-tab');
        const panels = document.querySelectorAll('[data-tab-panel]');
        panels.forEach((p) => {
          p.style.display = (p.getAttribute('data-tab-panel') === target) ? '' : 'none';
        });
      });
    });
  });

  // Chip / filter toggle (visual only)
  document.querySelectorAll('.chip-btn[data-toggle]').forEach((chip) => {
    chip.addEventListener('click', () => chip.classList.toggle('is-active'));
  });

  // Add-section button on Itinerary Builder — clones a blank section
  const addBtn = document.querySelector('.add-section-btn');
  const sectionsWrap = document.querySelector('[data-sections]');
  if (addBtn && sectionsWrap) {
    addBtn.addEventListener('click', () => {
      const sections = sectionsWrap.querySelectorAll('.builder-section');
      const template = sections[sections.length - 1];
      const clone = template.cloneNode(true);
      const newIndex = sections.length + 1;
      clone.querySelector('.sec-index').textContent = 'Section ' + newIndex;
      clone.querySelectorAll('input').forEach((i) => i.value = '');
      sectionsWrap.insertBefore(clone, addBtn);
    });
  }
});
