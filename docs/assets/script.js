function money(n) {
  return "$" + n.toFixed(2);
}

function productVisual(p) {
  if (p.image) {
    return `<img src="${p.image}" alt="${p.title} cover" loading="lazy" width="600" height="800">`;
  }
  return `<div class="merch-art" aria-label="${p.title}">${p.art.replace("\n", "<br>")}</div>`;
}

function guideCard(p) {
  return `
    <article class="card" data-category="${p.category}">
      <div class="card-image">
        ${productVisual(p)}
      </div>
      <div class="card-body">
        <div class="card-meta">${p.pages ? `${p.pages}-page PDF &middot; Instant download` : p.details}</div>
        <h3>${p.title}</h3>
        <p class="blurb">${p.blurb}</p>
        <div class="price-row">
          <span class="price">${money(p.price)}</span>
        </div>
        <a class="btn btn-card" href="${p.checkoutUrl}" data-product="${p.id}">${p.category === "goods" ? "Choose options" : "Get instant access"}</a>
      </div>
    </article>`;
}

function featuredCard(p) {
  const savePct = Math.round((1 - p.price / p.compareAt) * 100);
  return `
    <article class="card featured" data-category="${p.category}">
      <div class="card-image">
        ${productVisual(p)}
      </div>
      <div class="card-body">
        <div class="card-meta">${p.pages}-page PDF &middot; Most popular</div>
        <h3>${p.title}</h3>
        <p class="blurb">${p.blurb}</p>
        <div class="price-row">
          <span class="price">${money(p.price)}</span>
          <span class="compare-at">${money(p.compareAt)}</span>
          <span class="save-badge">Save ${savePct}%</span>
        </div>
        <a class="btn btn-card" href="${p.checkoutUrl}" data-product="${p.id}">Get the bundle</a>
      </div>
    </article>`;
}

function renderProducts() {
  const grid = document.getElementById("guides-grid");
  if (!grid || typeof PRODUCTS === "undefined") return;
  grid.innerHTML = PRODUCTS.map((p) => (p.featured ? featuredCard(p) : guideCard(p))).join("");
}

function setupFilters() {
  const buttons = document.querySelectorAll(".filter-btn");
  const grid = document.getElementById("guides-grid");
  if (!buttons.length || !grid) return;
  buttons.forEach((button) => button.addEventListener("click", () => {
    buttons.forEach((item) => item.classList.remove("active"));
    button.classList.add("active");
    const filter = button.dataset.filter;
    grid.querySelectorAll("[data-category]").forEach((card) => {
      card.hidden = filter !== "all" && card.dataset.category !== filter;
    });
  }));
}

function showToast(message) {
  let toast = document.querySelector(".toast");
  if (!toast) {
    toast = document.createElement("div");
    toast.className = "toast";
    document.body.appendChild(toast);
  }
  toast.textContent = message;
  toast.classList.add("show");
  clearTimeout(showToast._t);
  showToast._t = setTimeout(() => toast.classList.remove("show"), 3200);
}

function interceptPlaceholderCheckouts() {
  document.addEventListener("click", (e) => {
    const link = e.target.closest("a[data-product]");
    if (!link) return;
    if (link.getAttribute("href") === "#") {
      e.preventDefault();
      showToast("This product is ready for your checkout link. Add it in assets/products.js.");
    }
  });
}

function setupNav() {
  const toggle = document.querySelector(".nav-toggle");
  const header = document.querySelector(".site-header");
  if (!toggle || !header) return;
  toggle.addEventListener("click", () => {
    const open = header.classList.toggle("open");
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
  });
  header.querySelectorAll(".nav-links a").forEach((a) =>
    a.addEventListener("click", () => header.classList.remove("open"))
  );
}

function setYear() {
  const el = document.getElementById("year");
  if (el) el.textContent = new Date().getFullYear();
}

document.addEventListener("DOMContentLoaded", () => {
  renderProducts();
  setupFilters();
  interceptPlaceholderCheckouts();
  setupNav();
  setYear();
});
