var icon = document.getElementById("icon");

// Check if theme is already saved in localStorage
var savedTheme = localStorage.getItem("theme");
if (savedTheme) {
  document.documentElement.setAttribute("data-theme", savedTheme);
  if (savedTheme === "dark") {
    icon.src = "{{ url_for('static', filename='images/sun.png') }}";
  } else {
    icon.src = "{{ url_for('static', filename='images/moon.png') }}";
  }
}