// Small, dependency-free enhancements. Everything works without JS; this only adds motion.
(() => {
  const root = document.documentElement;
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  root.classList.add("js");

  // --- Theme toggle: follows the OS until the visitor picks one, then remembers it.
  const toggle = document.querySelector("[data-theme-toggle]");
  const systemDark = () => window.matchMedia("(prefers-color-scheme: dark)").matches;
  toggle?.addEventListener("click", () => {
    const current = root.dataset.theme || (systemDark() ? "dark" : "light");
    const next = current === "dark" ? "light" : "dark";
    root.dataset.theme = next;
    try { localStorage.setItem("theme", next); } catch (_) {}
  });

  const year = document.querySelector("[data-year]");
  if (year) year.textContent = new Date().getFullYear();

  // --- Header hairline, active nav link and timeline progress, all on one scroll handler.
  const header = document.querySelector(".site-header");
  const navLinks = [...document.querySelectorAll(".nav-links a")];
  const sections = navLinks.map((a) => document.querySelector(a.getAttribute("href"))).filter(Boolean);
  const jobs = document.querySelector(".jobs");

  const onScroll = () => {
    header?.classList.toggle("scrolled", window.scrollY > 8);

    const mid = window.innerHeight * 0.35;
    let active = null;
    for (const s of sections) if (s.getBoundingClientRect().top <= mid) active = s.id;
    navLinks.forEach((a) => a.classList.toggle("active", a.getAttribute("href") === `#${active}`));

    if (jobs && !reduceMotion) {
      const r = jobs.getBoundingClientRect();
      const p = (window.innerHeight * 0.75 - r.top) / r.height;
      jobs.style.setProperty("--progress", Math.min(1, Math.max(0, p)).toFixed(3));
    }
  };
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  // --- Reveal on scroll.
  const revealables = document.querySelectorAll(".reveal, .job");
  if (reduceMotion || !("IntersectionObserver" in window)) {
    revealables.forEach((el) => el.classList.add("is-visible"));
  } else {
    const io = new IntersectionObserver((entries) => {
      for (const e of entries) {
        if (e.isIntersecting) { e.target.classList.add("is-visible"); io.unobserve(e.target); }
      }
    }, { rootMargin: "0px 0px -10% 0px", threshold: 0.1 });
    revealables.forEach((el) => io.observe(el));
  }

  // --- Spotlight that follows the cursor on project cards.
  document.querySelectorAll(".project").forEach((card) => {
    card.addEventListener("pointermove", (e) => {
      const r = card.getBoundingClientRect();
      card.style.setProperty("--mx", `${e.clientX - r.left}px`);
      card.style.setProperty("--my", `${e.clientY - r.top}px`);
    });
  });

  // --- Project filters.
  const filters = document.querySelectorAll("[data-filter]");
  const cards = document.querySelectorAll("[data-tags]");
  filters.forEach((btn) => btn.addEventListener("click", () => {
    const f = btn.dataset.filter;
    filters.forEach((b) => b.setAttribute("aria-pressed", String(b === btn)));
    cards.forEach((card) => { card.hidden = f !== "all" && !card.dataset.tags.split(" ").includes(f); });
  }));

  // --- Contact form: sends through FormSubmit's AJAX endpoint and reports the real result.
  // Without JS the form still posts normally to FormSubmit, which redirects back via _next.
  const form = document.querySelector("[data-contact-form]");
  form?.addEventListener("submit", async (e) => {
    e.preventDefault();
    const status = form.querySelector(".form-status");
    const button = form.querySelector("button[type=submit]");
    const show = (msg, cls) => { status.textContent = msg; status.className = `form-status ${cls}`; };

    button.disabled = true;
    show(form.dataset.msgSending, "");
    try {
      const res = await fetch(form.action.replace("formsubmit.co/", "formsubmit.co/ajax/"), {
        method: "POST",
        headers: { Accept: "application/json" },
        body: new FormData(form),
      });
      const data = await res.json().catch(() => ({}));
      if (!res.ok || String(data.success) !== "true") throw new Error(data.message || res.status);
      form.reset();
      show(form.dataset.msgOk, "ok");
    } catch (err) {
      console.error("Contact form failed:", err);
      show(form.dataset.msgError, "error");
    } finally {
      button.disabled = false;
    }
  });

  if (reduceMotion) return;

  const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

  // --- Rotating role under the name.
  const rotator = document.querySelector("[data-rotate]");
  if (rotator) {
    const words = JSON.parse(rotator.dataset.rotate);
    const out = rotator.querySelector(".word");
    (async () => {
      for (let i = 0; ; i = (i + 1) % words.length) {
        const w = words[i];
        for (let n = 1; n <= w.length; n++) { out.textContent = w.slice(0, n); await sleep(45); }
        await sleep(1900);
        for (let n = w.length; n >= 0; n--) { out.textContent = w.slice(0, n); await sleep(22); }
        await sleep(250);
      }
    })();
  }

  // --- Terminal: type each command, then print its output.
  const term = document.querySelector("[data-terminal]");
  if (term) {
    const lines = [...term.querySelectorAll(".line")];
    const cursor = term.querySelector(".cursor-line");
    lines.forEach((l) => (l.hidden = true));
    if (cursor) cursor.hidden = true;

    const start = async () => {
      await sleep(400);
      for (const line of lines) {
        const typed = line.querySelector(".typed");
        if (typed) {
          const text = typed.textContent;
          typed.textContent = "";
          line.hidden = false;
          for (let n = 1; n <= text.length; n++) { typed.textContent = text.slice(0, n); await sleep(38 + Math.random() * 40); }
          await sleep(260);
        } else {
          line.hidden = false;
          await sleep(70);
        }
      }
      if (cursor) cursor.hidden = false;
    };

    const io = new IntersectionObserver((entries, obs) => {
      if (entries.some((e) => e.isIntersecting)) { obs.disconnect(); start(); }
    });
    io.observe(term);
  }
})();
