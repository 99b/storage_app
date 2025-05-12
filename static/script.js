// Function to change theme and save it to localStorage
function changeTheme() {
  const selectedTheme = document.getElementById('themeSelect').value;
  document.body.className = selectedTheme;  // Apply selected theme to the body

  // Save the selected theme in localStorage
  localStorage.setItem('theme', selectedTheme);
}

// Function to load the saved theme from localStorage (if exists)
function loadTheme() {
  const savedTheme = localStorage.getItem('theme');
  if (savedTheme) {
    // Set the theme on the dropdown and apply the saved theme
    document.getElementById('themeSelect').value = savedTheme;
    document.body.className = savedTheme;
  }
}

// Load theme on page load
window.onload = loadTheme;
