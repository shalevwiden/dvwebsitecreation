function neonizeButtons() {
  document.querySelectorAll("button").forEach((b) => {
    b.style.boxShadow = "0 0 12px #ff0000";
  });
}
neonizeButtons();
