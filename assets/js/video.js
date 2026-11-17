// Click-to-load video. Nothing is fetched from YouTube until a reader clicks a poster.
// The poster is then replaced by a youtube-nocookie.com iframe. The video id comes only from
// data-video-id and must match the pattern below; anything else does nothing.
// One delegated listener covers every video on the page, so the script binds once.
(function () {
  if (window.__ftrVideoBound) return;
  window.__ftrVideoBound = true;
  var ID_PATTERN = /^[A-Za-z0-9_-]{11}$/;

  function load(button) {
    var id = button.getAttribute("data-video-id") || "";
    if (!ID_PATTERN.test(id) || !button.parentNode) return;
    var frame = document.createElement("iframe");
    frame.setAttribute("src", "https://www.youtube-nocookie.com/embed/" + id + "?autoplay=1");
    frame.setAttribute("title", button.getAttribute("data-video-title") || "Video");
    frame.setAttribute("allow", "autoplay; encrypted-media; picture-in-picture");
    frame.setAttribute("allowfullscreen", "");
    frame.setAttribute("loading", "lazy");
    frame.setAttribute("referrerpolicy", "strict-origin-when-cross-origin");
    frame.className = "video-frame";
    button.parentNode.replaceChild(frame, button);
  }

  document.addEventListener("click", function (event) {
    var target = event.target;
    var button = target && target.closest ? target.closest(".video-poster") : null;
    if (button) load(button);
  });
})();
