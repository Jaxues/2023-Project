icon.onclick = function () {
  if (document.documentElement.getAttribute('data-theme') === 'light') {
    document.documentElement.setAttribute("data-theme", "dark");
    icon.src = "/static/images/light-svgrepo-com.svg";
    localStorage.setItem("theme", "dark");
  } else {
    document.documentElement.setAttribute("data-theme", "light");
    icon.src = "/static/images/dark-mode-night-moon-svgrepo-com.svg";
    localStorage.setItem("theme", "light");
  }
}
