document.addEventListener("DOMContentLoaded", () => {
  const overlay = document.createElement("div");
  overlay.className = "page-transition";
  document.body.appendChild(overlay);

  window.addEventListener("pageshow", () => {
    overlay.classList.remove("active");
  });

  document.querySelectorAll("a[href]").forEach(link => {
    const href = link.getAttribute("href");
    if (
      href &&
      !href.startsWith("#") &&
      !href.startsWith("javascript:") &&
      !link.hasAttribute("data-no-transition")
    ) {
      link.addEventListener("click", e => {
        if (e.metaKey || e.ctrlKey) return;
        e.preventDefault();
        overlay.classList.add("active");
        setTimeout(() => {
          window.location.href = href;
        }, 220);
      });
    }
  });

  document.querySelectorAll(".card-3d, .hero-3d-stage").forEach(card => {
    card.addEventListener("mousemove", e => {
      if (card.classList.contains("spin-3d-active")) return;
      const rect = card.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      const centerX = rect.width / 2;
      const centerY = rect.height / 2;
      const rotateX = ((y - centerY) / centerY) * -6;
      const rotateY = ((x - centerX) / centerX) * 6;
      card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.015, 1.015, 1.015)`;
    });
    card.addEventListener("mouseleave", () => {
      if (card.classList.contains("spin-3d-active")) return;
      card.style.transform = "perspective(1000px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)";
    });
  });

  setTimeout(() => {
    document.querySelectorAll(".flash-pill").forEach(el => {
      el.style.opacity = "0";
      el.style.transition = "opacity 0.4s ease";
      setTimeout(() => el.remove(), 400);
    });
  }, 3500);
});
