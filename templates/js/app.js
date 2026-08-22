// GlobeTrotter — Frontend Interactions & API Handlers

document.addEventListener('DOMContentLoaded', () => {

  // Mobile nav toggle
  const toggle = document.querySelector('.nav-toggle');
  const links = document.querySelector('.nav-links');
  if (toggle && links) {
    toggle.addEventListener('click', () => {
      links.classList.toggle('open');
    });
  }

  // Generic tab switcher: [data-tabs] -> [data-tab] and [data-tab-panel]
  document.querySelectorAll('[data-tabs]').forEach((group) => {
    const buttons = group.querySelectorAll('[data-tab]');
    buttons.forEach((btn) => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
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

  // Chip / filter toggle
  document.querySelectorAll('.chip-btn[data-toggle]').forEach((chip) => {
    chip.addEventListener('click', () => chip.classList.toggle('is-active'));
  });

  // Add-section button on Itinerary Builder
  const addBtn = document.querySelector('.add-section-btn');
  const sectionsWrap = document.querySelector('[data-sections]');
  if (addBtn && sectionsWrap) {
    addBtn.addEventListener('click', () => {
      const sections = sectionsWrap.querySelectorAll('.builder-section');
      const newIndex = sections.length + 1;
      
      const newSection = document.createElement('div');
      newSection.className = 'builder-section';
      newSection.innerHTML = `
        <span class="sec-index">Section ${newIndex}</span>
        <button type="button" class="btn btn-ghost btn-sm remove-section-btn" style="position:absolute;top:10px;right:14px;color:var(--coral);" onclick="this.closest('.builder-section').remove();">Remove</button>
        <div class="field" style="margin-top:10px;">
          <label class="small" style="font-weight:600;">Section Destination / Title</label>
          <input class="input" type="text" name="section_title[]" placeholder="e.g. Stop ${newIndex}" required />
        </div>
        <div class="field">
          <label class="small" style="font-weight:600;">Description</label>
          <textarea class="input" name="section_description[]" placeholder="Describe stops, accommodation, or activities..." style="min-height:70px;"></textarea>
        </div>
        <div class="builder-meta">
          <div class="meta-field">
            <label class="small" style="font-weight:600;">Date range</label>
            <input class="input mono" type="text" name="section_date_range[]" placeholder="Dates TBD" />
          </div>
          <div class="meta-field">
            <label class="small" style="font-weight:600;">Budget for this section</label>
            <input class="input mono" type="text" name="section_budget[]" placeholder="$500" />
          </div>
        </div>
      `;
      sectionsWrap.insertBefore(newSection, addBtn);
    });
  }

  // Community AJAX Like Handlers
  document.querySelectorAll('.like-btn').forEach((btn) => {
    btn.addEventListener('click', async (e) => {
      e.preventDefault();
      const postId = btn.getAttribute('data-post-id');
      if (!postId) return;

      try {
        const res = await fetch(`/community/${postId}/like`, {
          method: 'POST',
          headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'Accept': 'application/json'
          }
        });
        if (res.ok) {
          const data = await res.json();
          const countSpan = btn.querySelector('.like-count');
          if (countSpan && data.likes_count !== undefined) {
            countSpan.textContent = data.likes_count;
            btn.style.color = 'var(--coral)';
          }
        }
      } catch (err) {
        console.error('Like request failed:', err);
      }
    });
  });

});

// Global Modal Helpers
function openModal(id) {
  const modal = document.getElementById(id);
  if (modal) {
    modal.style.display = 'flex';
  }
}

function closeModal(id) {
  const modal = document.getElementById(id);
  if (modal) {
    modal.style.display = 'none';
  }
}

// Global Share Link Helper
function copyShareLink(url) {
  const fullUrl = window.location.origin + url;
  if (navigator.clipboard) {
    navigator.clipboard.writeText(fullUrl).then(() => {
      alert('Public itinerary link copied to clipboard:\n' + fullUrl);
    }).catch(() => {
      prompt('Copy this share link:', fullUrl);
    });
  } else {
    prompt('Copy this share link:', fullUrl);
  }
}

// Global Image Upload Preview Helper
function previewPhoto(input, previewId = 'photo-preview') {
  if (input.files && input.files[0]) {
    const reader = new FileReader();
    reader.onload = function(e) {
      const el = document.getElementById(previewId);
      if (el) {
        el.innerHTML = `<img src="${e.target.result}" style="width:100%;height:100%;object-fit:cover;border-radius:50%;display:block;" />`;
      }
    };
    reader.readAsDataURL(input.files[0]);
  }
}
