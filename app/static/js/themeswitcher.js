icon.onclick = function() {
  if (document.documentElement.getAttribute('data-theme') === 'light') {
    document.documentElement.setAttribute("data-theme", "dark");
    icon.src = "{{ url_for('static', filename='images/sun.png') }}";
    localStorage.setItem("theme", "dark"); 
  } else {
    document.documentElement.setAttribute("data-theme", "light");
    icon.src = "{{ url_for('static', filename='images/moon.png') }}";
    localStorage.setItem("theme", "light"); 
  }
}
