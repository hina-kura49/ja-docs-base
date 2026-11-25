/* 用語集: 本文の用語に点線の下線を引き、ホバー（スマホはタップ）で説明を出す。
   用語のデータは、別ファイル glossary-<団体>.js が window.JA_GLOSSARY に入れる。 */
(function () {
  var data = window.JA_GLOSSARY;
  if (!data || !data.length) return;

  var ROOTS = '.md-content__inner, .md-typeset, .doc, .document, .rst-content, article, main';
  var SKIP = 'code, pre, kbd, samp, script, style, textarea, a, h1, h2, h3, h4, h5, h6, .code-block, .headerlink, [data-glossary], .md-nav, nav';
  var root = document.querySelector(ROOTS);
  if (!root) return;

  function esc(s) { return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); }
  function head(ja) { return ja.replace(/（.*$/, '').replace(/\(.*$/, '').trim(); }

  // 一致させる語 → 項目。長い語を先に試す。
  var map = {}, names = [];
  data.forEach(function (e) {
    [e.ja && head(e.ja), e.term].concat(e.aliases || []).forEach(function (n) {
      if (n && !map[n.toLowerCase()]) { map[n.toLowerCase()] = e; names.push(n); }
    });
  });
  names.sort(function (a, b) { return b.length - a.length; });
  var ascii = /^[\x00-\x7f]+$/;
  var parts = names.map(function (n) {
    var b = ascii.test(n) ? ['(?<![A-Za-z0-9_-])', '(?![A-Za-z0-9_-])'] : ['', ''];
    return b[0] + esc(n) + b[1];
  });
  // 英字は、大文字小文字を区別しない（ASLR と aslr の両方に付く）
  var re = new RegExp('(' + parts.join('|') + ')', 'gi');

  var seen = {};
  var walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
    acceptNode: function (n) {
      if (!n.nodeValue.trim()) return NodeFilter.FILTER_REJECT;
      return n.parentNode.closest(SKIP) ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT;
    }
  });
  var nodes = [];
  while (walker.nextNode()) nodes.push(walker.currentNode);

  nodes.forEach(function (node) {
    var text = node.nodeValue, last = 0, out = null, m;
    re.lastIndex = 0;
    while ((m = re.exec(text))) {
      var e = map[m[0].toLowerCase()];
      if (!e || seen[e.term]) continue;       // 同じページでは、最初の 1 回だけ
      seen[e.term] = true;
      out = out || document.createDocumentFragment();
      out.appendChild(document.createTextNode(text.slice(last, m.index)));
      var s = document.createElement('span');
      s.className = 'ja-term';
      s.setAttribute('data-glossary', e.term);
      s.tabIndex = 0;
      s.textContent = m[0];
      out.appendChild(s);
      last = m.index + m[0].length;
    }
    if (out) {
      out.appendChild(document.createTextNode(text.slice(last)));
      node.parentNode.replaceChild(out, node);
    }
  });

  // 説明の吹き出し（1 つを使い回す）
  var byTerm = {};
  data.forEach(function (e) { byTerm[e.term] = e; });
  var tip = document.createElement('div');
  tip.className = 'ja-term-tip';
  tip.setAttribute('role', 'tooltip');
  tip.hidden = true;
  document.body.appendChild(tip);

  function show(el) {
    var e = byTerm[el.getAttribute('data-glossary')];
    if (!e) return;
    tip.textContent = '';
    var t = document.createElement('strong'); t.textContent = e.ja || e.term; tip.appendChild(t);
    var d = document.createElement('div'); d.textContent = e.desc; tip.appendChild(d);
    if (e.url) {
      var a = document.createElement('a'); a.href = e.url; a.target = '_blank'; a.rel = 'noopener';
      a.textContent = '詳しく見る'; tip.appendChild(a);
    }
    tip.hidden = false;
    var r = el.getBoundingClientRect(), w = tip.offsetWidth, h = tip.offsetHeight;
    var x = Math.max(8, Math.min(window.innerWidth - w - 8, r.left + r.width / 2 - w / 2));
    var y = r.top - h - 8 < 8 ? r.bottom + 8 : r.top - h - 8;
    tip.style.left = x + window.pageXOffset + 'px';
    tip.style.top = y + window.pageYOffset + 'px';
    tip.setAttribute('data-for', e.term);
  }
  function hide() { tip.hidden = true; }

  var hideTimer;
  root.addEventListener('mouseover', function (ev) {
    var el = ev.target.closest && ev.target.closest('.ja-term');
    if (el) { clearTimeout(hideTimer); show(el); }
  });
  root.addEventListener('mouseout', function (ev) {
    if (ev.target.closest && ev.target.closest('.ja-term')) hideTimer = setTimeout(hide, 200);
  });
  tip.addEventListener('mouseenter', function () { clearTimeout(hideTimer); });
  tip.addEventListener('mouseleave', hide);
  root.addEventListener('focusin', function (ev) { if (ev.target.classList.contains('ja-term')) show(ev.target); });
  root.addEventListener('focusout', hide);
  // スマホ: 用語をタップで開き、ほかをタップで閉じる
  document.addEventListener('click', function (ev) {
    var el = ev.target.closest && ev.target.closest('.ja-term');
    if (el) show(el); else if (!tip.contains(ev.target)) hide();
  });
  document.addEventListener('keydown', function (ev) { if (ev.key === 'Escape') hide(); });
})();
