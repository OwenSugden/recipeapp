document.addEventListener("scroll", function () {
  const navbar = document.querySelector(".navbar");
  const hero = document.querySelector(".hero"); // or your hero section class/id
  if (!navbar || !hero) return;

  const heroHeight = hero.offsetHeight;
  const fadeStart = heroHeight * 0.1;
  const fadeEnd = heroHeight * 0.6;

  const scrollY = window.scrollY;

  if (scrollY <= fadeStart) {
    navbar.style.background = "rgba(53, 79, 82, 1)";
  } else if (scrollY >= fadeEnd) {
    navbar.style.background = "rgba(53, 79, 82, 0.3)";
  } else {
    const progress = (scrollY - fadeStart) / (fadeEnd - fadeStart);
    const opacity = 1 - (0.7 * progress);
    navbar.style.background = `rgba(53, 79, 82, ${opacity})`;
  }
});