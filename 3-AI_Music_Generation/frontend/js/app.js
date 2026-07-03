// =========================
// GSAP LANDING PAGE
// =========================

window.addEventListener("DOMContentLoaded", () => {

  // Hero Animation
  const tl = gsap.timeline();

  tl.from(".badge", {
    y: 30,
    opacity: 0,
    duration: 0.8
  })

  .from(".hero-title", {
    y: 80,
    opacity: 0,
    duration: 1,
    ease: "power4.out"
  }, "-=0.4")

  .from(".hero-subtitle", {
    y: 40,
    opacity: 0,
    duration: 0.8
  }, "-=0.5")

  .from(".primary-btn, .secondary-btn", {
    y: 20,
    opacity: 0,
    stagger: 0.15,
    duration: 0.6
  }, "-=0.4")

  .from(".hero-card", {
    scale: 0.8,
    opacity: 0,
    duration: 1
  }, "-=1");

});

// =========================
// FLOATING PARTICLES
// =========================

for (let i = 0; i < 20; i++) {

  const particle = document.createElement("div");

  particle.style.position = "fixed";
  particle.style.width = Math.random() * 8 + 4 + "px";
  particle.style.height = particle.style.width;

  particle.style.borderRadius = "999px";

  particle.style.background =
    "rgba(255,255,255,0.15)";

  particle.style.left =
    Math.random() * 100 + "vw";

  particle.style.top =
    Math.random() * 100 + "vh";

  particle.style.pointerEvents = "none";

  particle.style.zIndex = "-1";

  document.body.appendChild(particle);

  gsap.to(particle, {
    y: -300,
    duration: 12 + Math.random() * 8,
    repeat: -1,
    ease: "none"
  });

}

// =========================
// NAVBAR SHADOW
// =========================

window.addEventListener("scroll", () => {

  const nav = document.querySelector("nav");

  if (!nav) return;

  if (window.scrollY > 30) {

    nav.classList.add("shadow-2xl");

  } else {

    nav.classList.remove("shadow-2xl");

  }

});