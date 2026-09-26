/**
 * Product catalog for the Hileenlove storefront.
 * Edit prices/descriptions here, and set each `checkoutUrl` to a real
 * payment link (see docs/README.md) to go live with sales.
 */
const PRODUCTS = [
  {
    id: "bundle",
    category: "digital",
    featured: true,
    title: "The Restaurant Worker's Survival Bundle",
    subtitle: "All six guides, one download",
    blurb:
      "Every guide in the Front-of-House Series in one 91-page download — earn more, protect your peace, and stand up for yourself at work.",
    pages: 91,
    price: 36.99,
    compareAt: 62.94,
    image: "assets/images/00-front-of-house-complete-bundle-cover.png",
    checkoutUrl: "#",
  },
  {
    id: "01-tips-and-income",
    category: "digital",
    title: "How to Increase Your Tips and Income",
    blurb:
      "A server and bartender playbook: the tip formula, upsell scripts that don't feel pushy, section strategy, and a 30-day income growth plan.",
    pages: 15,
    price: 9.99,
    image: "assets/images/01-increase-your-tips-and-income-cover.png",
    checkoutUrl: "#",
  },
  {
    id: "02-preventing-burnout",
    category: "digital",
    title: "Preventing Burnout in the Restaurant Industry",
    blurb:
      "Spot the 5 stages of burnout early, build a post-shift decompression routine, and set boundaries that actually hold.",
    pages: 15,
    price: 9.99,
    image: "assets/images/02-preventing-burnout-in-the-restaurant-industry-cover.png",
    checkoutUrl: "#",
  },
  {
    id: "03-document-mistreatment",
    category: "digital",
    title: "How to Document Mistreatment from Management",
    blurb:
      "Step-by-step help recording what's happening, protecting yourself, and knowing where to turn — with printable incident logs and templates.",
    pages: 17,
    price: 12.99,
    image: "assets/images/03-how-to-document-mistreatment-from-management-cover.png",
    checkoutUrl: "#",
  },
  {
    id: "04-essential-skills",
    category: "digital",
    title: "Essential Skills Every Front-of-House Worker Needs",
    blurb:
      "The 12 core FOH skills, the 10 steps of service, allergy protocol, and the HEARD method for difficult guests. Great for new hires.",
    pages: 17,
    price: 9.99,
    image: "assets/images/04-essential-skills-every-front-of-house-worker-needs-cover.png",
    checkoutUrl: "#",
  },
  {
    id: "05-communication-conflict",
    category: "digital",
    title: "Restaurant Communication and Workplace Conflict",
    blurb:
      "The STOP technique for heated moments mid-rush, scripts for coworker and manager conflicts, and a conflict resolution planner.",
    pages: 13,
    price: 9.99,
    image: "assets/images/05-restaurant-communication-and-workplace-conflict-cover.png",
    checkoutUrl: "#",
  },
  {
    id: "06-outcasted",
    category: "digital",
    title: "Dealing with Being Outcasted and Treated Differently",
    blurb:
      "Tell favoritism apart from discrimination and retaliation, address it with your manager, and build your next move.",
    pages: 13,
    price: 9.99,
    image: "assets/images/06-dealing-with-being-outcasted-and-treated-differently-cover.png",
    checkoutUrl: "#",
  },
  {
    id: "made-to-keep-tee",
    category: "goods",
    title: "Made to Keep Going Tee",
    blurb: "A soft everyday tee for long shifts, fresh starts, and the days you make your own rules.",
    details: "Print-on-demand · Unisex fit · Sizes S–3XL",
    price: 28.00,
    art: "KEEP\nGOING",
    checkoutUrl: "#",
  },
  {
    id: "soft-life-tote",
    category: "goods",
    title: "Soft Life, Strong Boundaries Tote",
    blurb: "A roomy carryall for your notebook, your essentials, and the boundary you finally kept.",
    details: "Print-on-demand · Cotton canvas · 15 × 16 in",
    price: 24.00,
    art: "SOFT LIFE\nSTRONG BOUNDARIES",
    checkoutUrl: "#",
  },
];
