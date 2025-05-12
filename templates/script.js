// Function to change color and save it to localStorage
function changeColor() {
  const selectedColor = document.getElementById('colorPicker').value;
  document.getElementById('title').style.color = selectedColor;

  // Save the color in localStorage
  localStorage.setItem('titleColor', selectedColor);
}

// Function to load saved color (if exists)
function loadColor() {
  const savedColor = localStorage.getItem('titleColor');
  if (savedColor) {
    document.getElementById('title').style.color = savedColor;
    document.getElementById('colorPicker').value = savedColor;
  }
}

// Run loadColor when page loads
window.onload = loadColor;
