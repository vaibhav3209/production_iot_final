document.addEventListener('DOMContentLoaded', function () {
    // ===============================
    // Elements
    // ===============================
    const overlay = document.getElementById('requestSidebarOverlay');
    const toggleBtn = document.getElementById('toggleSidebarBtn');
    const sidebar = document.getElementById('requestSidebar');
    const closeBtn = document.getElementById('closeSidebar');
    const componentList = document.getElementById('selected-components-list');
    const formHiddenFields = document.getElementById('form-hidden-fields');
    const clearBtn = document.getElementById('clearListBtn');

    // ===============================
    // Render Selected Components
    // ===============================
    function renderSelectedComponents() {
        const selected = JSON.parse(localStorage.getItem('selectedComponents') || '[]');
        componentList.innerHTML = '';
        formHiddenFields.innerHTML = '';

        if (selected.length === 0) {
            componentList.innerHTML = '<p>No components selected.</p>';
            return;
        }

        selected.forEach((item) => {
            const name = item.name || `Component ID: ${item.id}`;
            const quantity = item.quantity || 1;

            // Render in sidebar form
            componentList.innerHTML += `
                <div class="mb-2 border-bottom pb-2">
                    <p><strong>${name}</strong> - ${quantity}</p>
                </div>
            `;

            // Add hidden inputs for POST
            formHiddenFields.innerHTML += `
                <input type="hidden" name="component_ids[]" value="${item.id}">
                <input type="hidden" name="quantities[]" value="${quantity}">
            `;
        });
    }

    // ===============================
    // Clear localStorage via cookie
    // ===============================
    const shouldClear = document.cookie.split('; ').find(row => row.startsWith('clearLocalStorage='));
    if (shouldClear) {
        localStorage.removeItem('selectedComponents');
        document.cookie = "clearLocalStorage=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    }

    // ===============================
    // Page load: render components & project
    // ===============================
    renderSelectedComponents();

    // ===============================
    // Sidebar open
    // ===============================
    toggleBtn.addEventListener('click', function () {
        overlay.classList.add('active');

        renderSelectedComponents();
    });

    // ===============================
    // Sidebar close
    // ===============================
    closeBtn.addEventListener('click', function () {
        overlay.classList.remove('active');
    });

    // ===============================
    // Clear button
    // ===============================
    clearBtn.addEventListener('click', function () {
        localStorage.removeItem('selectedComponents');
        renderSelectedComponents();
    });
});