function money(n) {
  return "$" + n.toFixed(2);
}

function guideCard(p) {
  return `
    <article class="card">
      <div class="card-image">
        <img src="${p.image}" alt="${p.title} cover" loading="lazy" width="600" height="800">
      </div>
      <div class="card-body">
        <div class="card-meta">${p.pages}-page PDF &middot; Instant download</div>
        <h3>${p.title}</h3>
        <p class="blurb">${p.blurb}</p>
        <div class="price-row">
          <span class="price">${money(p.price)}</span>
        </div>
        <a class="btn btn-card" href="${p.checkoutUrl}" data-product="${p.id}">Buy Now</a>
      </div>
    </article>`;
}

function featuredCard(p) {
  const savePct = Math.round((1 - p.price / p.compareAt) * 100);
  return `
    <article class="card featured">
      <div class="card-image">
        <img src="${p.image}" alt="${p.title} cover" loading="lazy" width="600" height="800">
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
        <a class="btn btn-card" href="${p.checkoutUrl}" data-product="${p.id}">Get the Bundle</a>
      </div>
    </article>`;
}

function renderProducts() {
  const grid = document.getElementById("guides-grid");
  if (!grid || typeof PRODUCTS === "undefined") return;
  grid.innerHTML = PRODUCTS.map((p) => (p.featured ? featuredCard(p) : guideCard(p))).join("");
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
      showToast("Checkout isn't connected yet — add a payment link in assets/products.js.");
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
  interceptPlaceholderCheckouts();
  setupNav();
  setYear();
});
