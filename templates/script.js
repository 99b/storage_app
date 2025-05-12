// Function to change theme and save it to localStorage
function changeTheme() {
  const selectedTheme = document.getElementById('themeSelect').value;
  document.body.className = selectedTheme;  // Add class to body to switch theme
  
  // Save the theme in localStorage
  localStorage.setItem('theme', selectedTheme);
}

// Function to load the saved theme from localStorage (if exists)
function loadTheme() {
  const savedTheme = localStorage.getItem('theme');
  if (savedTheme) {
    document.getElementById('themeSelect').value = savedTheme;  // Select saved theme in dropdown
    document.body.className = savedTheme;  // Apply saved theme to body
  }
}

// Run loadTheme when page loads
window.onload = loadTheme;
