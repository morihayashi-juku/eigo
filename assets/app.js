/* 中1英語 教材棚 — 画面と印刷
   教材の中身は data/*.json に書く（このファイルは画面の仕組みだけ）。 */
"use strict";
pdfjsLib.GlobalWorkerOptions.workerSrc = "lib/pdfjs/pdf.worker.min.js";

const TRACKS = ["futari", "hitori"];
const PRINT_DPI = 200;               // 印刷用に描くときの細かさ
const $ = (s, el = document) => el.querySelector(s);
const esc = s => String(s ?? "").replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const P = f => "pdf/" + f;
const ICON_PRINT = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M6 9V3h12v6M6 18H4a1 1 0 0 1-1-1v-6a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v6a1 1 0 0 1-1 1h-2"/><rect x="6" y="14" width="12" height="7"/></svg>';
const ICON_DL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M12 3v12M7 10l5 5 5-5M4 19h16"/></svg>';
const dlLink = (it, cls, inner) => `<a class="${cls}" href="${esc(P(it.file))}" download="${esc(it.file)}" data-dl="${esc(it.file)}" title="PDFをダウンロード" aria-label="${esc(it.title)}のPDFをダウンロード">${inner}</a>`;
const ICON_CHEV = '<svg class="chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg>';

let D = null;                         // {common, futari, hitori}
const ITEMS = new Map();              // file → item（データ全体から）

/* ------------------------------------------------------------ 保存（この端末だけ） */
const store = {
  get(k, d) { try { const v = localStorage.getItem(k); return v == null ? d : JSON.parse(v); } catch (e) { return d; } },
  set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} },
};
let checks = store.get("eigo-shelf", {}) || {};
const isDone = (track, set) => D[track].checks.every(([k]) => checks[set.id + "-" + k]);

/* ------------------------------------------------------------ データ */
async function loadData() {
  const get = n => fetch(`data/${n}.json`, {cache: "no-cache"}).then(r => {
    if (!r.ok) throw new Error(`data/${n}.json が読めません（${r.status}）`);
    return r.json();
  });
  const [common, futari, hitori] = await Promise.all(["common", "futari", "hitori"].map(get));
  D = {common, futari, hitori};
  for (const t of TRACKS) {
    for (const it of [...(D[t].common || []), ...(D[t].old || [])]) ITEMS.set(it.file, it);
    for (const s of D[t].sets) for (const g of s.groups) for (const it of g.items) ITEMS.set(it.file, it);
  }
  $("#updated").textContent = common.updated ? `最終更新 ${common.updated.replace(/^(\d+)-0?(\d+)-0?(\d+)$/, "$1年$2月$3日")}` : "";
}
const unitOf = id => D.common.units.find(u => u.id === id);
const unitName = id => (unitOf(id) || {name: id}).name;

/* ------------------------------------------------------------ 部品 */
function tile(it) {
  const many = it.pages > 1 ? " stack" : "";
  return `<div class="tile">
    <button type="button" class="open" data-act="view" data-file="${esc(it.file)}" aria-label="${esc(it.title)}を見る">
      <span class="thumb${many}" data-thumb="${esc(it.file)}"><span class="pg">${it.pages}p</span></span>
      <span class="t">${esc(it.title)}</span>${it.note ? `<span class="n">${esc(it.note)}</span>` : ""}
    </button>
    <div class="tacts">
      <button type="button" class="btn pr" data-act="print" data-file="${esc(it.file)}">${ICON_PRINT}印刷</button>
      ${dlLink(it, "btn dl", ICON_DL + "PDF")}
    </div>
  </div>`;
}

function setCard(track, s, {open = false, showWho = false, anchor = true} = {}) {
  const T = D[track];
  const prog = T.checks.map(([k, l]) => `<i class="${checks[s.id + "-" + k] ? "on" : ""}" title="${esc(l)}"></i>`).join("");
  const units = (s.units || []).map(u => `<span>${esc((unitOf(u) || {}).short || u)}</span>`).join("");
  return `<details class="set${s.cur ? " cur" : ""}"${anchor ? ` id="${track}-${esc(s.id)}"` : ""} data-track="${track}" data-set="${esc(s.id)}"${open ? " open" : ""}>
  <summary>
    <span class="sno">${esc(s.label)}</span>
    <span class="stitle">${esc(s.title)}</span>
    <span class="prog" aria-label="進み具合">${prog}${ICON_CHEV}</span>
    <span class="smeta">${s.cur ? '<span class="tag">今ここ</span>' : ""}${showWho ? `<span class="who">${esc(T.name)}</span>` : ""}${units}</span>
  </summary>
  <div class="sbody">
    ${s.words && s.words.length ? `<div class="words" aria-label="単語">${s.words.map(w => `<span>${esc(w)}</span>`).join("")}</div>` : ""}
    ${s.note ? `<p class="note">${esc(s.note)}</p>` : ""}
    <div class="groups">${s.groups.map(g => `<section class="group ${esc(g.kind)}"><h3>${esc(g.label)}</h3><div class="tiles">${g.items.map(tile).join("")}</div></section>`).join("")}</div>
    <div class="sfoot">
      <div class="chk">${T.checks.map(([k, l]) => `<label><input type="checkbox" data-act="check" data-key="${esc(s.id)}-${k}"${checks[s.id + "-" + k] ? " checked" : ""}>${esc(l)}</label>`).join("")}</div>
      <button type="button" class="btn primary" data-act="printset" data-track="${track}" data-set="${esc(s.id)}">${ICON_PRINT}${esc(s.label)}をまとめて印刷</button>
    </div>
  </div>
</details>`;
}

const rowList = (items, cls = "") => `<ul class="rows ${cls}">${items.map(it => `<li>
  <button type="button" class="r" data-act="view" data-file="${esc(it.file)}"><b>${esc(it.title)}</b><small>${it.pages}ページ${it.note ? "　" + esc(it.note) : ""}</small></button>
  <button type="button" class="p" data-act="print" data-file="${esc(it.file)}" aria-label="${esc(it.title)}を印刷">${ICON_PRINT}</button>
  ${dlLink(it, "p", ICON_DL)}</li>`).join("")}</ul>`;

/* ------------------------------------------------------------ 画面：2人／新しく入った子 */
let filter = store.get("eigo-filter2", {});
function renderTrack(track) {
  const T = D[track];
  const sets = [...T.sets].reverse();                    // 新しい順
  const cur = T.sets.find(s => s.cur) || T.sets[T.sets.length - 1];
  const used = [...new Set(T.sets.flatMap(s => s.units || []))];
  const f = filter[track] || "all";
  const shown = sets.filter(s => f === "all" || (f === "todo" ? !isDone(track, s) : (s.units || []).includes(f)));
  const curUnit = cur && cur.units && cur.units[0] ? unitName(cur.units[0]) : "";
  return `
  ${cur ? `<section class="now" aria-label="今の位置">
    <span class="lab">今ここ　${esc(T.longName)}</span>
    <span class="no">${esc(cur.label)}</span>
    <div><h1>${esc(cur.title)}</h1><div class="nu">${esc(curUnit)}</div></div>
    <div class="acts">
      <button type="button" class="btn key" data-act="printset" data-track="${track}" data-set="${esc(cur.id)}">${ICON_PRINT}${esc(cur.label)}をまとめて印刷</button>
      <a class="btn" href="#${track}/${esc(cur.id)}">${esc(cur.label)}の教材を見る</a>
    </div>
  </section>` : ""}
  <div class="layout">
    <div>
      <div class="filters" role="group" aria-label="しぼりこみ">
        ${[["all", "すべて"], ...used.map(u => [u, (unitOf(u) || {}).short || u]), ["todo", "まだ終わっていない"]]
          .map(([k, l]) => `<button type="button" data-act="filter" data-track="${track}" data-f="${esc(k)}" aria-pressed="${f === k}">${esc(l)}</button>`).join("")}
      </div>
      <div class="sets">${shown.map(s => setCard(track, s, {open: s === cur})).join("") || '<p class="empty">この条件の教材はありません。</p>'}</div>
    </div>
    <aside class="side">
      ${T.about ? `<div class="panel"><h2>${esc(T.longName)}</h2>${T.about.map(p => `<p>${esc(p)}</p>`).join("")}</div>` : ""}
      ${T.common && T.common.length ? `<div class="panel"><h2>ずっと使うもの</h2>${rowList(T.common)}</div>` : ""}
      ${T.old && T.old.length ? `<div class="panel"><h2>過去の版</h2>${rowList(T.old, "old")}</div>` : ""}
    </aside>
  </div>`;
}

/* ------------------------------------------------------------ 画面：単元別 */
function renderUnits() {
  const units = D.common.units;
  return `
  <nav class="unav" aria-label="単元">${units.map(u => `<a href="#tangen/${esc(u.id)}">${esc(u.short)}</a>`).join("")}</nav>
  ${units.map(u => `<section class="unit" id="unit-${esc(u.id)}">
    <h2>${esc(u.name)}</h2>
    <div class="ucols">${TRACKS.map(t => {
      const sets = D[t].sets.filter(s => (s.units || []).includes(u.id));
      return `<div class="ucol"><h3>${esc(D[t].longName)}</h3>
        <div class="sets">${sets.map(s => setCard(t, s, {anchor: false})).join("") || '<p class="empty">この単元の教材はまだありません。</p>'}</div></div>`;
    }).join("")}</div>
  </section>`).join("")}`;
}

/* ------------------------------------------------------------ 画面の切りかえ */
function route() {
  const [tab, sub] = (location.hash.replace(/^#/, "") || store.get("eigo-tab", "futari")).split("/");
  const t = ["futari", "hitori", "tangen"].includes(tab) ? tab : "futari";
  store.set("eigo-tab", t);
  document.querySelectorAll(".tabs a").forEach(a => {
    if (a.dataset.tab === t) a.setAttribute("aria-current", "page"); else a.removeAttribute("aria-current");
  });
  $("#app").innerHTML = t === "tangen" ? renderUnits() : renderTrack(t);
  document.title = {futari: "2人", hitori: "新しく入った子", tangen: "単元別"}[t] + " | 中1英語 教材棚";
  if (sub) {
    const el = t === "tangen" ? $("#unit-" + CSS.escape(sub)) : $(`#${t}-${CSS.escape(sub)}`);
    if (el) { if (el.tagName === "DETAILS") el.open = true; el.scrollIntoView({block: "start"}); window.scrollBy(0, -64); }
  } else window.scrollTo(0, 0);
  observeThumbs();
}

/* ------------------------------------------------------------ PDF を読む・描く */
const docs = new Map();
function getDoc(file) {
  if (!docs.has(file)) {
    const p = pdfjsLib.getDocument({url: P(file)}).promise;
    p.catch(() => docs.delete(file));
    docs.set(file, p);
  }
  return docs.get(file);
}
async function drawPage(file, n, cssWidth, ratio) {
  const doc = await getDoc(file);
  const page = await doc.getPage(n);
  const base = page.getViewport({scale: 1});
  const vp = page.getViewport({scale: (cssWidth * ratio) / base.width});
  const c = document.createElement("canvas");
  c.width = Math.ceil(vp.width); c.height = Math.ceil(vp.height);
  const ctx = c.getContext("2d");
  ctx.fillStyle = "#fff"; ctx.fillRect(0, 0, c.width, c.height);
  await page.render({canvasContext: ctx, viewport: vp}).promise;
  return c;
}

/* サムネイル：見えたものから順に、2つずつ描く */
const thumbQueue = []; let thumbBusy = 0;
const thumbIO = "IntersectionObserver" in window ? new IntersectionObserver(es => {
  for (const e of es) if (e.isIntersecting) { thumbIO.unobserve(e.target); thumbQueue.push(e.target); }
  pumpThumbs();
}, {rootMargin: "200px"}) : null;
function observeThumbs() {
  document.querySelectorAll(".thumb[data-thumb]:not([data-done])").forEach(el => thumbIO ? thumbIO.observe(el) : thumbQueue.push(el));
  if (!thumbIO) pumpThumbs();
}
function pumpThumbs() {
  while (thumbBusy < 2 && thumbQueue.length) {
    const el = thumbQueue.shift();
    if (el.dataset.done) continue;
    el.dataset.done = "1"; thumbBusy++;
    drawPage(el.dataset.thumb, 1, el.clientWidth || 118, Math.min(window.devicePixelRatio || 1, 2))
      .then(c => el.prepend(c)).catch(() => { el.insertAdjacentHTML("afterbegin", '<span class="muted" style="padding:6px;display:block">読めません</span>'); })
      .finally(() => { thumbBusy--; pumpThumbs(); });
  }
}
document.addEventListener("toggle", e => { if (e.target.matches && e.target.matches("details[open]")) observeThumbs(); }, true);

/* ------------------------------------------------------------ ビューア */
const viewer = $("#viewer");
let viewing = null, viewIO = null;
async function openViewer(file) {
  const it = ITEMS.get(file) || {file, title: file, pages: "?"};
  viewing = it;
  $("#v-title").textContent = it.title;
  $("#v-pages").textContent = "";
  $("#v-open").href = P(file);
  $("#v-dl").href = P(file); $("#v-dl").setAttribute("download", file); $("#v-dl").dataset.dl = file;
  const body = $("#v-body");
  body.innerHTML = "";
  if (!viewer.open) viewer.showModal();
  body.scrollTop = 0;
  try {
    const doc = await getDoc(file);
    if (viewing !== it) return;
    $("#v-pages").textContent = `${doc.numPages}ページ`;
    if (viewIO) viewIO.disconnect();
    viewIO = new IntersectionObserver(es => {
      for (const e of es) if (e.isIntersecting && !e.target.dataset.done) {
        e.target.dataset.done = "1";
        drawPage(file, +e.target.dataset.n, e.target.clientWidth, Math.min(window.devicePixelRatio || 1, 2) * 1.25)
          .then(c => e.target.prepend(c)).catch(() => {});
      }
    }, {root: body, rootMargin: "400px"});
    for (let i = 1; i <= doc.numPages; i++) {
      const d = document.createElement("div");
      d.className = "v-page"; d.dataset.n = i; d.setAttribute("aria-label", `${i}ページ目`);
      body.append(d); viewIO.observe(d);
    }
  } catch (e) {
    body.innerHTML = `<p class="v-err">このPDFを開けませんでした（pdf/${esc(file)}）。ファイル名がまちがっていないか確認してください。</p>`;
  }
}
$("#v-close").addEventListener("click", () => viewer.close());
$("#v-print").addEventListener("click", () => viewing && printJob(viewing.title, [{file: viewing.file, copies: 1}]));
viewer.addEventListener("close", () => { if (viewIO) viewIO.disconnect(); $("#v-body").innerHTML = ""; viewing = null; });

/* ------------------------------------------------------------ まとめて印刷 */
const sp = $("#setprint");
let spRows = [];
function openSetPrint(track, id) {
  const s = D[track].sets.find(x => x.id === id);
  if (!s) return;
  $("#sp-title").textContent = `${s.label}「${s.title}」をまとめて印刷`;
  spRows = [];
  let html = "";
  for (const g of s.groups) {
    html += `<li class="g ${esc(g.kind)}">${esc(g.label)}</li>`;
    for (const it of g.items) {
      const i = spRows.push({it, on: (it.copies ?? 1) > 0, copies: Math.max(it.copies ?? 1, 1)}) - 1;
      html += `<li><input type="checkbox" id="sp${i}" data-i="${i}"${spRows[i].on ? " checked" : ""}>
        <label class="nm" for="sp${i}">${esc(it.title)}<small>${it.pages}ページ${it.note ? "　" + esc(it.note) : ""}</small></label>
        <span class="step"><button type="button" data-i="${i}" data-d="-1" aria-label="${esc(it.title)}の部数をへらす">−</button><span id="spc${i}">${spRows[i].copies}部</span><button type="button" data-i="${i}" data-d="1" aria-label="${esc(it.title)}の部数をふやす">＋</button></span></li>`;
    }
  }
  $("#sp-list").innerHTML = html;
  spTotal();
  sp.showModal();
  sp.dataset.title = `${s.label} ${s.title}`;
}
function spTotal() {
  const n = spRows.reduce((a, r) => a + (r.on ? r.it.pages * r.copies : 0), 0);
  $("#sp-total").textContent = `合計 ${n}ページ`;
  $("#sp-go").disabled = n === 0;
  $("#sp-go").textContent = n ? `${n}ページを印刷する` : "印刷する";
}
$("#sp-list").addEventListener("change", e => { const i = e.target.dataset.i; if (i != null) { spRows[i].on = e.target.checked; spTotal(); } });
$("#sp-list").addEventListener("click", e => {
  const b = e.target.closest("button[data-d]"); if (!b) return;
  const r = spRows[b.dataset.i];
  r.copies = Math.min(9, Math.max(1, r.copies + +b.dataset.d)); r.on = true;
  $("#spc" + b.dataset.i).textContent = r.copies + "部"; $("#sp" + b.dataset.i).checked = true; spTotal();
});
$("#sp-cancel").addEventListener("click", () => sp.close());
$("#sp-go").addEventListener("click", () => {
  const jobs = spRows.filter(r => r.on).map(r => ({file: r.it.file, copies: r.copies}));
  sp.close();
  printJob(sp.dataset.title, jobs);
});

/* ------------------------------------------------------------ 印刷のしくみ
   PDF をページごとに画像にして #print-root にならべ、ブラウザの印刷を呼ぶ。
   （別のタブを開かずに、何ファイルでも1回で印刷できる。部数ぶんページをくり返す） */
const pageImg = new Map();                    // "file#n" → blob URL（一度描いたら使い回す）
const progress = $("#progress");
let printing = false;
let lastJobs = [];
const TOUCH = navigator.maxTouchPoints > 1;     // iPad・iPhone など
async function renderForPrint(file, n) {
  const k = file + "#" + n;
  if (pageImg.has(k)) return pageImg.get(k);
  const doc = await getDoc(file);
  const page = await doc.getPage(n);
  const base = page.getViewport({scale: 1});
  const c = await drawPage(file, n, base.width, PRINT_DPI / 72);
  const url = await new Promise(res => c.toBlob(b => res(URL.createObjectURL(b)), "image/png"));
  c.width = c.height = 0;
  pageImg.set(k, url);
  return url;
}
async function printJob(title, jobs) {
  if (printing || !jobs.length) return;
  printing = true; lastJobs = jobs;
  if (viewer.open) viewer.close();
  $("#pg-title").textContent = "印刷の準備をしています";
  $("#pg-btns").hidden = true; $("#pg-again").hidden = false; $("#pg-bar").style.width = "0"; $("#pg-text").textContent = "";
  progress.showModal();
  const root = $("#print-root");
  root.innerHTML = "";
  try {
    const docsN = await Promise.all(jobs.map(j => getDoc(j.file).then(d => d.numPages)));
    const total = docsN.reduce((a, n) => a + n, 0);
    const sheets = docsN.reduce((a, n, i) => a + n * jobs[i].copies, 0);
    let done = 0;
    const urls = [];
    for (let j = 0; j < jobs.length; j++) {
      const list = [];
      for (let n = 1; n <= docsN[j]; n++) {
        list.push(await renderForPrint(jobs[j].file, n));
        done++;
        $("#pg-bar").style.width = (100 * done / total) + "%";
        $("#pg-text").textContent = `${done} / ${total} ページ（印刷するのは全部で ${sheets} ページ）`;
      }
      for (let c = 0; c < jobs[j].copies; c++) urls.push(...list);
    }
    const frag = document.createDocumentFragment();
    const imgs = urls.map(u => { const d = document.createElement("div"); d.className = "sheet"; const im = new Image(); im.src = u; im.alt = ""; d.append(im); frag.append(d); return im; });
    root.append(frag);
    await Promise.all(imgs.map(im => im.decode ? im.decode().catch(() => {}) : null));
    progress.close();
    doPrint(title);
    $("#pg-title").textContent = "印刷の用意ができました";
    $("#pg-text").textContent = `全部で ${sheets} ページ。印刷画面が出ないとき（iPad など）は、下の「${TOUCH ? "PDFで印刷" : "印刷画面を開く"}」を押してください。${TOUCH ? "出てきた画面で「プリント」を選びます。" : ""}部数は印刷画面ではなく、ここでえらんだ部数になっています。`;
    $("#pg-btns").hidden = false; $("#pg-share").hidden = !TOUCH;
    progress.showModal();
  } catch (e) {
    $("#pg-title").textContent = "印刷の準備ができませんでした";
    $("#pg-text").textContent = "PDF が読めませんでした。ページを読みこみなおして、もう一度ためしてください。";
    $("#pg-btns").hidden = false; $("#pg-again").hidden = true;
  } finally { printing = false; }
}
function doPrint(title) {
  const old = document.title;
  document.title = title || old;              // 「PDFに保存」のときのファイル名になる
  try { window.print(); } finally { setTimeout(() => { document.title = old; }, 500); }
}
$("#pg-again").addEventListener("click", () => { progress.close(); doPrint(); setTimeout(() => { if (!progress.open) progress.showModal(); }, 1500); });
/* iPad で window.print() が効かないとき：PDF そのものを共有画面に出し、そこから「プリント」を選ぶ */
$("#pg-share").addEventListener("click", async () => {
  const btn = $("#pg-share"), old = btn.textContent; btn.disabled = true; btn.textContent = "PDFを用意しています…";
  try {
    const files = [];
    for (const j of lastJobs) {
      const blob = await (await fetch(P(j.file))).blob();
      for (let c = 0; c < j.copies; c++) files.push(new File([blob], (c ? c + "_" : "") + j.file, {type: "application/pdf"}));
    }
    if (navigator.canShare && navigator.canShare({files})) await navigator.share({files});
    else if (lastJobs[0]) window.open(P(lastJobs[0].file), "_blank");
  } catch (e) { /* 共有をやめたとき */ }
  btn.disabled = false; btn.textContent = old;
});
$("#pg-close").addEventListener("click", () => { progress.close(); $("#pg-again").hidden = false; });
window.__eigoPrintJob = printJob;             // 動作確認用

/* ------------------------------------------------------------ PDF の保存
   iPad・iPhone は、ふつうのダウンロードだと PDF を開くだけで保存されない。
   タッチ端末では「共有」の画面（ファイルに保存・AirDrop など）を出して、そこから保存できるようにする。 */
async function savePdf(file) {
  try {
    if (TOUCH && navigator.canShare && navigator.share) {
      const blob = await (await fetch(P(file))).blob();
      const f = new File([blob], file, {type: "application/pdf"});
      if (navigator.canShare({files: [f]})) { await navigator.share({files: [f]}); return true; }
    }
  } catch (e) { if (e && e.name === "AbortError") return true; }   // 共有をやめたときは何もしない
  return false;                                                      // 使えなければふつうのダウンロード
}
document.addEventListener("click", async e => {
  const a = e.target.closest("a[data-dl]");
  if (!a || !a.dataset.dl) return;
  e.preventDefault();
  if (!(await savePdf(a.dataset.dl))) { const t = document.createElement("a"); t.href = a.href; t.download = a.dataset.dl; document.body.append(t); t.click(); t.remove(); }
});

/* ------------------------------------------------------------ 操作 */
document.addEventListener("click", e => {
  const b = e.target.closest("[data-act]");
  if (!b || b.tagName === "INPUT") return;
  const act = b.dataset.act;
  if (act === "view") openViewer(b.dataset.file);
  else if (act === "print") { const it = ITEMS.get(b.dataset.file); printJob(it ? it.title : b.dataset.file, [{file: b.dataset.file, copies: 1}]); }
  else if (act === "printset") { e.preventDefault(); openSetPrint(b.dataset.track, b.dataset.set); }
  else if (act === "filter") {
    filter[b.dataset.track] = b.dataset.f; store.set("eigo-filter2", filter);
    $("#app").innerHTML = renderTrack(b.dataset.track); observeThumbs();
  }
});
document.addEventListener("change", e => {
  const k = e.target.dataset && e.target.dataset.key;
  if (!k) return;
  checks[k] = e.target.checked; store.set("eigo-shelf", checks);
  const card = e.target.closest("details.set");
  if (card) {
    const T = D[card.dataset.track];
    card.querySelectorAll(".prog i").forEach((i, n) => i.classList.toggle("on", !!checks[card.dataset.set + "-" + T.checks[n][0]]));
  }
});
window.addEventListener("hashchange", route);

loadData().then(route).catch(err => {
  $("#app").innerHTML = `<p class="v-err">教材の一覧を読みこめませんでした：${esc(err.message)}</p>`;
});
