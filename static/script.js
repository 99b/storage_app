// Function to change theme and save it to localStorage
function changeTheme() {
  const selectedTheme = document.getElementById('themeSelect').value;
  document.body.className = selectedTheme;  // Apply the selected theme to the body

  // Apply the theme to other page elements if necessary (like <h1>)
  const titleElement = document.getElementById('title');
  titleElement.className = selectedTheme;  // Set the theme class on h1

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

    // Apply the theme to other page elements (like <h1>)
    const titleElement = document.getElementById('title');
    titleElement.className = savedTheme;
  }
}

// Load theme on page load
window.onload = loadTheme;
