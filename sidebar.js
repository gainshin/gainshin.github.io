/**
 * Sidebar Navigation Component
 * Handles rendering and interactivity of the sidebar across all reports.
 */

const sidebarNavData = [
    {
        group: "Overview",
        id: "overview",
        collapsible: false,
        items: [
            { href: "Research.html", icon: "home", label: "Welcome", id: "welcome" },
            { href: "Framework.html", icon: "network", label: "Research Framework", id: "framework" },
        ]
    },
    {
        group: "Weekly Reports",
        id: "weekly-reports",
        collapsible: true,
        items: [
            { href: "Week1to3_report.html", icon: "file-text", label: "Week 1-3 Progress Report", id: "week1to3" },
            { href: "Week4_report.html", icon: "file-text", label: "Week 4 Progress Report", id: "week4" },
            { href: "Week5_report.html", icon: "file-text", label: "Week 5 Progress Report", id: "week5" },
            { href: "Week6_report.html", icon: "file-text", label: "Week 6 Progress Report", id: "week6" },
        ]
    },
    {
        group: "Bi-weekly Discussion",
        id: "biweekly-discussion",
        collapsible: true,
        items: [
            { href: "Bi-weekly-discussion.html", icon: "message-circle", label: "B: Heuristic Audit Tool (Wk 7-8)", id: "biweekly-wk78" },
        ]
    },
    {
        group: "Zotero Reports",
        id: "zotero-reports",
        collapsible: true,
        items: [
            { href: "Zotero_summary.html", icon: "library", label: "Library Status Summary", id: "zotero-summary" },
            { href: "Zotero_round1.html", icon: "bookmark", label: "Zotero Report (Round 1)", id: "zotero1" },
            { href: "Zotero_round2.html", icon: "bookmark", label: "Zotero Report (Round 2)", id: "zotero2" },
            { href: "Zotero_round3.html", icon: "bookmark", label: "Zotero Report (Round 3)", id: "zotero3" },
            { href: "Zotero_round4.html", icon: "bookmark", label: "Zotero Report (Round 4)", id: "zotero4" },
            { href: "Zotero_round5.html", icon: "bookmark", label: "Zotero Report (Round 5)", id: "zotero5" },
            { href: "Zotero_round6.html", icon: "bookmark", label: "Zotero Report (Round 6)", id: "zotero6" },
            { href: "Zotero_5C.html", icon: "scan-search", label: "5C Decomposition", id: "zotero-5c" },
        ]
    },
    {
        group: "Deliverables",
        id: "deliverables",
        collapsible: true,
        items: [
            { href: "INFS_611_poster.html", icon: "presentation", label: "Research Proposal Poster", id: "infs611-poster" },
        ]
    },
];

function renderSidebar(activePageId) {
    const sidebar = document.getElementById('sidebar');
    if (!sidebar) return;

    // Inject CSS for sidebar
    const style = document.createElement('style');
    style.textContent = `
        /* Sidebar Styles */
        .sidebar-section {
            padding: 8px 0;
            border-bottom: 1px solid var(--border-color);
        }
        
        .sidebar-section:last-child {
            border-bottom: none;
        }

        .sidebar-section-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 8px 14px;
            cursor: pointer;
            user-select: none;
            color: var(--text-tertiary);
            transition: color 0.2s;
        }

        .sidebar-section-header:hover {
            color: var(--text-primary);
        }
        
        .sidebar-section-title {
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .sidebar-section-toggle {
            transition: transform 0.2s;
            width: 14px;
            height: 14px;
        }

        .sidebar-section.collapsed .sidebar-section-toggle {
            transform: rotate(-90deg);
        }

        .sidebar-nav-container {
            overflow: hidden;
            transition: max-height 0.3s ease-out, opacity 0.3s ease-out;
            max-height: 1000px; /* Arbitrary large height */
            opacity: 1;
        }

        .sidebar-section.collapsed .sidebar-nav-container {
            max-height: 0;
            opacity: 0;
        }
        
        /* Adjust footer to be at bottom */
        .sidebar-footer {
            margin-top: auto;
        }
    `;
    document.head.appendChild(style);

    // Build HTML
    let html = `
        <div class="sidebar-header">
            <img src="assets/joshua.png" alt="Joshua" class="logo">
            <span class="title">Research Notes</span>
        </div>
        <div style="flex: 1; overflow-y: auto;">
    `;

    sidebarNavData.forEach(group => {
        // Determine if this group contains the active page
        const hasActiveItem = group.items.some(item => item.id === activePageId);

        // Determine initial collapsed state
        // If it has active item -> expanded
        // If it's not collapsible -> expanded
        // Otherwise -> collapsed by default (unless specific logic requires otherwise)
        let isCollapsed = group.collapsible && !hasActiveItem;

        // Overview is never collapsed
        if (group.id === 'overview') isCollapsed = false;

        const collapsedClass = isCollapsed ? 'collapsed' : '';
        const toggleIcon = group.collapsible ?
            `<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="sidebar-section-toggle"><polyline points="6 9 12 15 18 9"></polyline></svg>` :
            '';

        const headerCursor = group.collapsible ? 'cursor: pointer;' : 'cursor: default;';

        html += `
            <div class="sidebar-section ${collapsedClass}" id="group-${group.id}">
                <div class="sidebar-section-header" style="${headerCursor}" ${group.collapsible ? `onclick="toggleSidebarGroup('${group.id}')"` : ''}>
                    <span class="sidebar-section-title">${group.group}</span>
                    ${toggleIcon}
                </div>
                <div class="sidebar-nav-container">
                    <nav>
        `;

        group.items.forEach(item => {
            const isActive = item.id === activePageId ? 'active' : '';

            // Special handling for Research.html Welcome link
            // If we are currently ON Research.html (activePageId === 'welcome'), 
            // the link should handle the internal tab switching if needed, 
            // OR if it's just a link to Research.html, it works fine as is.
            // The original Research.html had href="#" and data-doc-id="welcome".
            // However, since we are unifying, standardizing on href="Research.html" is cleaner 
            // unless we are strictly in SPA mode on that page.
            // Let's check if the current page is Research.html by checking window.location or just use standard links.
            // If we are on Research.html, clicking "Welcome" should probably just reload or do nothing if already active.
            // But Research.html has specific logic for "data-doc-id".

            // Refined logic: If we are on Research.html, we might want to preserve the SPA-like behavior for "Welcome".
            // But looking at the plan, we want to replace the hardcoded sidebar.
            // If the user clicks "Welcome" from another page, they go to Research.html.
            // If they are on Research.html, they are already there.

            // For now, use standard hrefs. If specific SPA behavior is needed for Research.html, 
            // we can add an event listener there or check if activePageId is 'welcome'.

            let href = item.href;
            let extraAttrs = '';

            if (activePageId === 'welcome' && item.id === 'welcome') {
                href = '#';
                extraAttrs = 'data-doc-id="welcome"';
            }

            html += `
                <a href="${href}" class="sidebar-nav-item ${isActive}" ${extraAttrs}>
                    <i data-lucide="${item.icon}"></i>
                    <span>${item.label}</span>
                </a>
            `;
        });

        html += `
                    </nav>
                </div>
            </div>
        `;
    });

    html += `</div>`; // Close flex container

    // Footer
    html += `
        <div class="sidebar-footer">
            <a href="index.html">
                <i data-lucide="arrow-left"></i>
                Back to Portfolio
            </a>
        </div>
    `;

    sidebar.innerHTML = html;

    // Initialize icons
    if (window.lucide) {
        window.lucide.createIcons();
    }
}

function toggleSidebarGroup(groupId) {
    const group = document.getElementById(`group-${groupId}`);
    if (group) {
        group.classList.toggle('collapsed');
    }
}
