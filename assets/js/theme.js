// Theme toggle. Without this script the OS setting (prefers-color-scheme) still applies.
// Storage can throw in private windows; then the choice lasts for this page only.
(function () {
  var root = document.documentElement;
  var btn = document.getElementById("theme-toggle");
  if (!btn) return;
  function saved() { try { var v = localStorage.getItem("theme"); return v === "light" || v === "dark" ? v : null; } catch (e) { return null; } }
  function save(t) { try { localStorage.setItem("theme", t); } catch (e) { return; } }
  var dark = window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
  var current = saved() || (dark ? "dark" : "light");
  function apply() {
    root.setAttribute("data-theme", current);
    btn.setAttribute("aria-pressed", current === "dark" ? "true" : "false");
  }
  apply();
  btn.hidden = false;
  btn.addEventListener("click", function () {
    current = current === "dark" ? "light" : "dark";
    apply();
    save(current);
  });
})();
