/**
 * Shared series nav for audit/*.html
 * Literacy-shell chrome; does not write :root tokens (pages own --ink etc).
 */
const AUDIT_PAGES = [
  { id: 'prd', href: 'Audit_PRD.html', label: 'PRD' },
  { id: 'method', href: 'Audit_method.html', label: 'Method' },
  { id: 'console', href: 'Audit_interface_console.html', label: 'Console' },
  { id: 'result', href: 'rejara-iesult_sample.html', label: 'Result sample' },
  { id: 'workbench', href: 'audit-workbench.html', label: 'Workbench' },
];

const AUDIT_SIDEBAR_CSS = `
html,body{height:100%;overflow:hidden}
body{display:flex;margin:0}

.side-nav{
  --sn-ink:#1D1D1B;--sn-red:#E3120B;--sn-rule:#D4D1CB;--sn-mid:#6B6B6B;
  --sn-bg2:#f7f7f5;--sn-hover:#ebebea;--sn-ter:#9b9a97;
  width:260px;min-width:260px;height:100vh;
  background:var(--sn-bg2);border-right:1px solid var(--sn-rule);
  display:flex;flex-direction:column;overflow:hidden;flex-shrink:0;
  font-family:'Inter',-apple-system,'PingFang TC','Noto Sans TC',sans-serif;
}
.side-nav-header{
  padding:12px 14px;border-bottom:1px solid var(--sn-rule);
  font-size:14px;font-weight:600;color:var(--sn-ink);flex-shrink:0;
}
.side-nav-scroll{flex:1;overflow-y:auto;padding:8px 0}
.side-nav .nav-group{
  font-size:11px;font-weight:600;letter-spacing:.5px;text-transform:uppercase;
  color:var(--sn-ter);padding:8px 14px 6px;
}
.side-nav a{
  display:block;color:var(--sn-mid);text-decoration:none;font-weight:500;
  font-size:14px;padding:6px 14px;border:0;background:transparent;border-radius:0;
}
.side-nav a:hover{background:var(--sn-hover);color:var(--sn-ink)}
.side-nav a.active{background:var(--sn-hover);color:var(--sn-ink);font-weight:600}
.side-nav-footer{
  padding:12px 14px;border-top:1px solid var(--sn-rule);flex-shrink:0;
}
.side-nav-footer a{
  display:flex;align-items:center;gap:8px;font-size:13px;color:var(--sn-mid);
  padding:0;font-weight:500;
}
.side-nav-footer a:hover{background:transparent;color:var(--sn-ink)}

.main-content{
  flex:1;min-width:0;display:flex;flex-direction:column;overflow:hidden;
  border-top:3px solid #E3120B;
}
.page-chrome{
  --sn-ink:#1D1D1B;--sn-red:#E3120B;--sn-rule:#D4D1CB;--sn-mid:#6B6B6B;
  display:flex;align-items:center;justify-content:space-between;gap:12px;
  padding:12px 24px;flex-shrink:0;
  background:#fff;border-bottom:1px solid #D4D1CB;
  font-family:'Inter',-apple-system,'PingFang TC','Noto Sans TC',sans-serif;
}
.main-body{flex:1;overflow-y:auto;padding:40px 60px;scroll-behavior:smooth}
.main-body.is-app{padding:0}
.main-body.is-app:has(.app){overflow:hidden}
.main-body.is-app .app{height:100%}
.breadcrumbs{display:flex;align-items:center;gap:6px;font-size:.76rem;color:#9b9a97}
.breadcrumbs a{color:#6B6B6B;text-decoration:none;font-weight:600}
.breadcrumbs a:hover{color:#E3120B}
.breadcrumbs .sep{color:#D4D1CB}
.breadcrumbs .current{color:#1D1D1B;font-weight:700}
.view-only-badge{
  display:inline-flex;align-items:center;gap:4px;
  font-size:.66rem;font-weight:800;letter-spacing:.08em;text-transform:uppercase;
  color:#6B6B6B;border:1px solid #D4D1CB;padding:.2rem .5rem;background:#fff;
}
.view-only-badge svg{width:12px;height:12px;flex-shrink:0}

@media(max-width:768px){
  html,body{height:auto;overflow:auto}
  body{flex-direction:column}
  .side-nav{width:100%;min-width:0;height:auto;border-right:0;border-bottom:1px solid #D4D1CB}
  .side-nav-scroll{display:flex;flex-wrap:wrap;padding:8px 8px 12px}
  .side-nav .nav-group{width:100%;padding:8px 6px 4px}
  .side-nav a{padding:6px 10px}
  .main-content{border-top:0}
  .main-body{padding:24px 16px}
  .main-body.is-app{padding:0}
  .page-chrome{padding:12px 16px}
  body:has(.main-body.is-app){height:100%;overflow:hidden}
  body:has(.main-body.is-app) .side-nav{flex-shrink:0}
}
@media print{
  html,body{height:auto;overflow:visible}
  body{display:block}
  .side-nav,.page-chrome{display:none}
}
`;

const LOCK_SVG = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>`;

function injectAuditSidebarCSS() {
  if (document.getElementById('audit-sidebar-css')) return;
  const style = document.createElement('style');
  style.id = 'audit-sidebar-css';
  style.textContent = AUDIT_SIDEBAR_CSS;
  document.head.appendChild(style);
}

function renderAuditChrome(activeId) {
  const el = document.getElementById('audit-chrome');
  if (!el) return;
  const page = AUDIT_PAGES.find(p => p.id === activeId);
  const label = page ? page.label : '';
  el.innerHTML = `
    <nav class="breadcrumbs" aria-label="Breadcrumb">
      <a href="../index.html">Home</a>
      <span class="sep">/</span>
      <a href="../index.html#products">AI prototypes</a>
      <span class="sep">/</span>
      <span class="current">${label}</span>
    </nav>
    <span class="view-only-badge">${LOCK_SVG} View Only</span>
  `;
}

function renderAuditSidebar(activePageId) {
  injectAuditSidebarCSS();
  const nav = document.getElementById('audit-sidebar');
  if (nav) {
    const links = AUDIT_PAGES.map(p =>
      `<a href="${p.href}"${p.id === activePageId ? ' class="active" aria-current="page"' : ''}>${p.label}</a>`
    ).join('');
    nav.innerHTML = `
      <div class="side-nav-header">Interface Audit</div>
      <div class="side-nav-scroll">
        <div class="nav-group">Pages</div>
        ${links}
      </div>
      <div class="side-nav-footer">
        <a href="../index.html#products">← Back to Portfolio</a>
      </div>
    `;
  }
  renderAuditChrome(activePageId);
}
