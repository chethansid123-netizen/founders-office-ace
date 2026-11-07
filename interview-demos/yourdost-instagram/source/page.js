/* Showcase page: draws the ten posts from creatives.js (the same renderer the exports use). */
(function () {
  "use strict";
  const { POSTS, frameHTML } = window.JBN;
  const esc = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  const reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // Keep a 1080px-wide creative scaled to its container.
  function fit(screen, scaler) {
    const apply = () => { const w = screen.clientWidth; if (w) scaler.style.transform = `scale(${w / 1080})`; };
    apply();
    if ("ResizeObserver" in window) new ResizeObserver(apply).observe(screen);
    else window.addEventListener("resize", apply);
  }
  function screenEl(post) {
    const screen = document.createElement("div");
    screen.className = "screen " + (post.tall ? "tall" : "feed");
    const scaler = document.createElement("div");
    scaler.className = "scaler";
    screen.appendChild(scaler);
    fit(screen, scaler);
    return { screen, scaler };
  }

  // ---------- profile grid (newest first, as Instagram shows it) ----------
  function buildGrid() {
    const host = document.getElementById("grid9");
    const feed = POSTS.filter((p) => p.kind !== "story").slice().reverse();
    feed.forEach((p) => {
      const b = document.createElement("button");
      b.type = "button";
      b.setAttribute("aria-label", `Go to post ${p.id}, ${p.title}`);
      const fake = { tall: false };
      const s = screenEl(fake);
      // reels show their cover, cropped to the 4:5 grid tile like Instagram does
      if (p.kind === "reel") {
        s.scaler.innerHTML = frameHTML(p);
        s.scaler.style.top = "-21.1%"; // centre the 9:16 cover in a 4:5 tile
      } else {
        s.scaler.innerHTML = frameHTML(p, 0);
      }
      b.appendChild(s.screen);
      b.insertAdjacentHTML("beforeend", `<span class="n">${p.id}</span><span class="kind">${p.kind}</span>`);
      b.addEventListener("click", () => document.getElementById("post-" + p.id).scrollIntoView({ behavior: reduce ? "auto" : "smooth" }));
      host.appendChild(b);
    });
  }

  // ---------- the ten lines ----------
  function buildLines() {
    const host = document.getElementById("lines10");
    host.innerHTML = POSTS.map((p) => `
      <li><a href="#post-${p.id}">
        <div class="top"><span class="num">${p.id}</span><span class="pg-chips"><span>${esc(p.date)}</span><span>${esc(p.theme)}</span><span>${esc(p.format.split(" ·")[0].split(" +")[0])}</span></span></div>
        <p class="said">${esc(p.line)}</p>
        <p class="unsaid">${esc(p.line2)}</p>
        ${p.en ? `<p class="en">${esc(p.en)}</p>` : ""}
      </a></li>`).join("");
  }

  // ---------- players ----------
  function reelPlayer(post, wrap) {
    const { screen, scaler } = screenEl(post);
    const shell = document.createElement("div");
    shell.className = "shell";
    shell.appendChild(screen);
    const bar = document.createElement("div");
    bar.className = "progress";
    bar.innerHTML = "<i></i>";
    const ctr = document.createElement("div");
    ctr.className = "controls";
    ctr.innerHTML = `<button type="button" class="pp">Play</button><button type="button" class="rs">Restart</button><span class="status"></span>`;
    wrap.append(shell, bar, ctr);
    const dur = post.reel.dur;
    let t = post.reel.cover, playing = false, visible = false, last = 0, drawn = -1;
    const pp = ctr.querySelector(".pp"), st = ctr.querySelector(".status"), fill = bar.firstChild;
    const draw = () => {
      scaler.innerHTML = frameHTML(post, 0, t);
      fill.style.width = (100 * t / dur).toFixed(2) + "%";
      st.textContent = `${t.toFixed(1)} / ${dur.toFixed(1)} s`;
    };
    const setPlay = (v) => { playing = v; pp.textContent = v ? "Pause" : "Play"; last = 0; if (v) requestAnimationFrame(tick); };
    function tick(ts) {
      if (!playing) return;
      if (visible) {
        if (last) t += Math.min(0.1, (ts - last) / 1000);
        last = ts;
        if (t >= dur) t = 0;
        if (ts - drawn > 30) { draw(); drawn = ts; }
      } else last = 0;
      requestAnimationFrame(tick);
    }
    pp.addEventListener("click", () => setPlay(!playing));
    ctr.querySelector(".rs").addEventListener("click", () => { t = 0; draw(); if (!playing) setPlay(true); });
    screen.addEventListener("click", () => setPlay(!playing));
    draw();
    if ("IntersectionObserver" in window) {
      new IntersectionObserver((es) => es.forEach((e) => {
        visible = e.isIntersecting;
        if (visible && !playing && !reduce && !wrap.dataset.touched) { wrap.dataset.touched = "1"; t = 0; setPlay(true); }
      }), { threshold: 0.55 }).observe(screen);
    }
  }

  function slidePlayer(post, wrap) {
    const n = post.slides.length;
    const { screen, scaler } = screenEl(post);
    const shell = document.createElement("div");
    shell.className = "shell";
    shell.style.position = "relative";
    shell.appendChild(screen);
    let i = 0;
    const story = post.kind === "story";
    let segs, dots;
    if (story) {
      segs = document.createElement("div");
      segs.className = "segs";
      segs.innerHTML = Array.from({ length: n }, () => "<i></i>").join("");
      screen.appendChild(segs);
      const tz = document.createElement("div");
      tz.className = "tapzone";
      tz.innerHTML = `<button type="button" aria-label="Previous frame"></button><button type="button" aria-label="Next frame"></button><button type="button" aria-label="Next frame"></button>`;
      screen.appendChild(tz);
      const bs = tz.querySelectorAll("button");
      bs[0].addEventListener("click", () => go(i - 1));
      bs[1].addEventListener("click", () => go(i + 1));
      bs[2].addEventListener("click", () => go(i + 1));
    }
    wrap.appendChild(shell);
    if (n > 1) {
      if (!story) {
        dots = document.createElement("div");
        dots.className = "dots";
        dots.innerHTML = Array.from({ length: n }, () => "<i></i>").join("");
        wrap.appendChild(dots);
      }
      const ctr = document.createElement("div");
      ctr.className = "controls";
      ctr.innerHTML = `<button type="button" class="pv" aria-label="Previous">←</button><button type="button" class="nx" aria-label="Next">→</button><span class="status"></span>`;
      wrap.appendChild(ctr);
      ctr.querySelector(".pv").addEventListener("click", () => go(i - 1));
      ctr.querySelector(".nx").addEventListener("click", () => go(i + 1));
      var st = ctr.querySelector(".status");
      // swipe
      let x0 = null;
      screen.addEventListener("pointerdown", (e) => { x0 = e.clientX; });
      screen.addEventListener("pointerup", (e) => { if (x0 === null) return; const dx = e.clientX - x0; x0 = null; if (Math.abs(dx) > 40) go(i + (dx < 0 ? 1 : -1)); });
      shell.tabIndex = 0;
      shell.setAttribute("aria-label", `${post.title}: use the arrow keys to change ${story ? "frame" : "slide"}`);
      shell.addEventListener("keydown", (e) => { if (e.key === "ArrowRight") { go(i + 1); e.preventDefault(); } if (e.key === "ArrowLeft") { go(i - 1); e.preventDefault(); } });
    }
    function go(k) {
      i = Math.max(0, Math.min(n - 1, k));
      scaler.innerHTML = frameHTML(post, i, null, { bare: false });
      if (dots) dots.querySelectorAll("i").forEach((d, j) => d.classList.toggle("on", j === i));
      if (segs) segs.querySelectorAll("i").forEach((d, j) => d.classList.toggle("on", j <= i));
      if (st) st.textContent = `${story ? "Frame" : "Slide"} ${i + 1} of ${n}`;
    }
    go(0);
  }

  // ---------- post rows ----------
  function buildPosts() {
    const host = document.getElementById("posts");
    POSTS.forEach((p) => {
      const row = document.createElement("article");
      row.className = "post";
      row.id = "post-" + p.id;
      const dev = document.createElement("div");
      dev.className = "device";
      row.appendChild(dev);
      const notes = document.createElement("div");
      notes.className = "notes";
      notes.innerHTML = `
        <div class="head">
          <span class="num">${p.id} of 10</span>
          <h3>${esc(p.title)}</h3>
          <div class="pg-chips"><span>${esc(p.theme)}</span><span>${esc(p.format)}</span><span>${esc(p.date)}, ${esc(p.time)}</span></div>
        </div>
        <div class="theline">
          <span class="label">The post</span>
          <p class="said">${esc(p.line)}</p>
          <p class="unsaid">${esc(p.line2)}</p>
          ${p.en ? `<p class="en">${esc(p.en)}</p>` : ""}
        </div>
        <p class="why"><b>Why:</b> ${esc(p.why)}</p>
        <dl class="facts-list">
          <dt>Who it's for</dt><dd>${esc(p.segment)}</dd>
          <dt>Hook</dt><dd>${esc(p.hook)}</dd>
          <dt>Engagement</dt><dd>${esc(p.mechanic)}</dd>
          <dt>Why it's human</dt><dd>${esc(p.human)}</dd>
          <dt>Measure</dt><dd>${esc(p.measure)}</dd>
        </dl>
        <div class="caption"><span class="label">Caption</span><pre id="cap-${p.id}">${esc(p.caption)}</pre><button type="button" data-cap="${p.id}">Copy</button></div>`;
      row.appendChild(notes);
      host.appendChild(row);
      if (p.kind === "reel") reelPlayer(p, dev); else slidePlayer(p, dev);
    });
    host.addEventListener("click", (e) => {
      const b = e.target.closest("button[data-cap]");
      if (!b) return;
      const pre = document.getElementById("cap-" + b.dataset.cap);
      const done = () => { b.textContent = "Copied"; setTimeout(() => (b.textContent = "Copy"), 1600); };
      const fallback = () => { const r = document.createRange(); r.selectNodeContents(pre); const s = getSelection(); s.removeAllRanges(); s.addRange(r); b.textContent = "Selected, press Ctrl+C"; };
      try { navigator.clipboard.writeText(pre.textContent).then(done, fallback); } catch (err) { fallback(); }
    });
  }

  // ---------- calendar ----------
  function buildCalendar() {
    const host = document.getElementById("cal-rows");
    host.innerHTML = POSTS.map((p) => `<tr><td>${esc(p.date)} · ${esc(p.time)}</td><td><a href="#post-${p.id}">${p.id} ${esc(p.title)}</a></td><td>${esc(p.format)}</td><td>${esc(p.segment)}</td><td>${esc(p.measure)}</td></tr>`).join("");
  }

  const start = () => {
    buildGrid();
    buildLines();
    buildPosts();
    buildCalendar();
  };
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(start, start); else start();
})();
