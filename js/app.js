/**
 * API 手册 - 单页应用
 * 导航数据来源：title/<manual>.yaml
 * 本地预览：python3 server.py 然后 http://localhost:8000
 */

// ============================================================
// marked.js + highlight.js 配置
// ============================================================

marked.use({
  renderer: {
    heading({ tokens, depth }) {
      const text = this.parser.parseInline(tokens);
      const id = text.replace(/<[^>]*>/g, '').trim();
      return `<h${depth} id="${id}">${text}</h${depth}>\n`;
    },
    code({ text, lang }) {
      const l = (lang || '').toLowerCase();
      if (l && hljs.getLanguage(l)) {
        const h = hljs.highlight(text, { language: l }).value;
        return `<pre><code class="hljs language-${l}">${h}</code></pre>\n`;
      }
      return `<pre><code>${escapeHtml(text)}</code></pre>\n`;
    }
  }
});

// ============================================================
// 状态
// ============================================================

let currentManual = null;
let navTree = [];
let mdCache = {};
const contentEl = document.getElementById('content');
let navEl;

// ============================================================
// 视图切换
// ============================================================

function showHome() {
  document.body.classList.add('home-view');
  history.pushState(null, '', window.location.pathname);
}

function showViewer() {
  document.body.classList.remove('home-view');
}

// ============================================================
// 导航渲染（depth: 0=section层, 1+=sub层）
// ============================================================

/**
 * 渲染一组节点到 container
 * depth=0 时 item 作为 .nav-section 包装
 * depth>=1 时 item 有 items → .nav-sub 可折叠；无 items → .nav-item 链接
 */
function renderItems(items, container, depth) {
  items.forEach(item => {
    if (depth === 0) {
      // ---- 一级分组 (.nav-section) ----
      const wrapper = document.createElement('div');
      wrapper.className = 'nav-section collapsed';
      const header = document.createElement('div');
      header.className = 'nav-section-header';
      header.innerHTML = `<span>${escapeHtml(item.title)}</span><span class="arrow">▼</span>`;
      header.addEventListener('click', () => wrapper.classList.toggle('collapsed'));
      wrapper.appendChild(header);
      const body = document.createElement('div');
      body.className = 'nav-section-items';
      if (item.items) renderItems(item.items, body, depth + 1);
      wrapper.appendChild(body);
      container.appendChild(wrapper);
      return;
    }

    // ---- depth >= 1 ----
    if (item.items) {
      const wrapper = document.createElement('div');
      wrapper.className = 'nav-sub collapsed';

      const header = document.createElement(item.file ? 'a' : 'span');
      header.className = 'nav-item group';
      if (item.file) {
        header.href = '#' + item.file;
        header.dataset.file = item.file;
      }
      header.innerHTML = `${escapeHtml(item.title)}<span class="arrow">▼</span>`;
      header.addEventListener('click', e => {
        if (item.file) {
          e.preventDefault();
          loadDoc(item.file);
          highlightNavItem(header);
        }
        wrapper.classList.toggle('collapsed');
        if (window.innerWidth <= 768) closeSidebar();
      });
      wrapper.appendChild(header);

      const body = document.createElement('div');
      body.className = 'nav-sub-body';
      renderItems(item.items, body, depth + 1);
      wrapper.appendChild(body);
      container.appendChild(wrapper);
    } else if (item.file) {
      // 叶子：有 file
      const el = document.createElement('a');
      el.className = 'nav-item';
      el.href = '#' + item.file;
      el.dataset.file = item.file;
      el.innerHTML = escapeHtml(item.title);
      el.addEventListener('click', e => {
        e.preventDefault();
        loadDoc(item.file);
        highlightNavItem(el);
        if (window.innerWidth <= 768) closeSidebar();
      });
      container.appendChild(el);
    } else {
      // 空目录：无 file 无 items，显示箭头
      const wrapper = document.createElement('div');
      wrapper.className = 'nav-sub collapsed';
      const header = document.createElement('span');
      header.className = 'nav-item group';
      header.innerHTML = `${escapeHtml(item.title)}<span class="arrow">▼</span>`;
      header.addEventListener('click', () => wrapper.classList.toggle('collapsed'));
      wrapper.appendChild(header);
      const body = document.createElement('div');
      body.className = 'nav-sub-body';
      wrapper.appendChild(body);
      container.appendChild(wrapper);
    }
  });
}

function renderNav(tree) {
  const nav = document.getElementById('sidebarNav');
  nav.innerHTML = '';
  renderItems(tree, nav, 0);
  navEl = nav;
}

function highlightNavItem(activeEl) {
  navEl.querySelectorAll('.nav-item.active').forEach(el => el.classList.remove('active'));
  if (activeEl) activeEl.classList.add('active');
}

// ============================================================
// 文档加载 & 渲染
// ============================================================

function parseFile(file) {
  const idx = file.indexOf('#');
  if (idx === -1) return { path: file, anchor: null };
  return { path: file.slice(0, idx), anchor: decodeURIComponent(file.slice(idx + 1)) };
}

async function loadDoc(file) {
  const { path, anchor } = parseFile(file);
  const cacheKey = currentManual + '/' + path;

  if (mdCache[cacheKey] == null) {
    try {
      const resp = await fetch('docs/' + cacheKey);
      if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
      mdCache[cacheKey] = await resp.text();
    } catch (err) {
      mdCache[cacheKey] = null;
      contentEl.innerHTML = loadFailHtml(path);
      return;
    }
  }

  if (mdCache[cacheKey] == null) return;

  showViewer();
  let html = marked.parse(mdCache[cacheKey]);

  // 修正图片路径
  const baseDir = path.includes('/') ? path.slice(0, path.lastIndexOf('/') + 1) : '';
  const imgBase = 'docs/' + currentManual + '/' + baseDir;
  html = html.replace(/(<img[^>]* src=")(\.\/)/g, '$1' + imgBase);

  contentEl.innerHTML = `<div class="markdown-body">${html}</div>`;
  history.pushState(null, '', '#' + file);

  // 双帧等待：确保大文件渲染布局完成后再滚动
  requestAnimationFrame(() => {
    requestAnimationFrame(() => {
      if (anchor) {
        const el = document.getElementById(anchor);
        if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
      } else {
        contentEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });
}

function loadFailHtml(path) {
  return `
    <div class="content-placeholder" style="padding:80px 20px;text-align:center">
      <h2>😵 加载失败</h2>
      <p>文件 <code>docs/${escapeHtml(path)}</code> 无法加载。</p>
      <p style="font-size:0.85rem;margin-top:1em;color:#565f89">请以 HTTP 方式打开（如 <code>python3 server.py</code>）。</p>
    </div>`;
}

// ============================================================
// 路由
// ============================================================

window.addEventListener('hashchange', () => {
  const hash = window.location.hash.slice(1);
  if (!hash) { showHome(); return; }
  showViewer();
  const navItem = navEl.querySelector(`.nav-item[data-file="${CSS.escape(hash)}"]`);
  if (navItem) {
    highlightNavItem(navItem);
    expandAncestors(navItem);
    loadDoc(hash);
  }
});

function expandAncestors(el) {
  let parent = el.parentElement;
  while (parent) {
    if (parent.classList.contains('nav-section')) parent.classList.remove('collapsed');
    if (parent.classList.contains('nav-sub')) parent.classList.remove('collapsed');
    parent = parent.parentElement;
  }
}

// ============================================================
// 移动端侧边栏
// ============================================================

function toggleSidebar() {
  const sb = document.getElementById('sidebar');
  const ov = document.getElementById('overlay');
  const open = sb.classList.toggle('open');
  ov.classList.toggle('show', open);
}

function closeSidebar() {
  document.getElementById('sidebar').classList.remove('open');
  document.getElementById('overlay').classList.remove('show');
}

document.getElementById('menuToggle').addEventListener('click', toggleSidebar);
document.getElementById('overlay').addEventListener('click', closeSidebar);

// ============================================================
// 工具
// ============================================================

function escapeHtml(str) {
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}

// ============================================================
// 启动
// ============================================================

document.querySelector('.back-home').addEventListener('click', () => showHome());

document.querySelectorAll('.manual-card').forEach(card => {
  card.addEventListener('click', async () => {
    const key = card.dataset.manual;
    const url = card.dataset.url;

    if (key === 'null') return;  // 约定：null 不跳转
    // 无 manual 但有 url → 跳官网
    if (!key && url) {
      window.open(url, '_blank');
      return;
    }
    if (!key) return;

    try {
      const resp = await fetch('title/' + key + '.yaml');
      if (!resp.ok) throw new Error('yaml not found');
      const yaml = jsyaml.load(await resp.text());
      currentManual = key;
      navTree = yaml.tree || [];
      mdCache = {};
      renderNav(navTree);

      const first = navEl.querySelector('.nav-item[data-file]');
      if (first) {
        highlightNavItem(first);
        expandAncestors(first);
        loadDoc(first.dataset.file);
      }
    } catch (err) {
      console.error('加载手册失败:', err);
    }
  });
});

// 加载官网链接，填入 data-url 并渲染 ↗ 图标
(async () => {
  try {
    const resp = await fetch('title/links.yaml');
    if (!resp.ok) return;
    const links = jsyaml.load(await resp.text());
    document.querySelectorAll('.manual-card').forEach(card => {
      // data-url 存的是 links.yaml 的 key，查表得到真实 URL
      const linkKey = card.dataset.url;
      if (linkKey && linkKey !== 'null' && links[linkKey]) {
        card.dataset.url = links[linkKey];
      }
      // 渲染 ↗ 图标（null 约定：无角标）
      if (card.dataset.url && card.dataset.url !== 'null') {
        const a = document.createElement('a');
        a.className = 'ext-link';
        a.href = card.dataset.url;
        a.target = '_blank';
        a.textContent = '↗';
        a.addEventListener('click', e => e.stopPropagation());
        card.appendChild(a);
      }
    });
  } catch (_) {}
})();

showHome();
