// Element toggle function
const elementToggleFunc = function (elem) {
  elem.classList.toggle("active");
}

// Sidebar variables
const sidebar = document.querySelector("[data-sidebar]");
const sidebarBtn = document.querySelector("[data-sidebar-btn]");

// Sidebar toggle functionality for mobile
sidebarBtn.addEventListener("click", function () {
  elementToggleFunc(sidebar);
});

// Tab navigation functionality
const navigationLinks = document.querySelectorAll("[data-nav-link]");
const pages = document.querySelectorAll("[data-page]");

// Add click event to all navigation links
for (let i = 0; i < navigationLinks.length; i++) {
  navigationLinks[i].addEventListener("click", function () {
    
    // Remove active class from all navigation links
    for (let j = 0; j < navigationLinks.length; j++) {
      navigationLinks[j].classList.remove("active");
    }
    
    // Add active class to clicked navigation link
    this.classList.add("active");
    
    // Get the data-page value of the corresponding page
    const currentPageId = this.innerHTML.toLowerCase().trim();
    
    // Remove active class from all pages
    for (let k = 0; k < pages.length; k++) {
      if (pages[k].dataset.page === currentPageId) {
        pages[k].classList.add("active");
      } else {
        pages[k].classList.remove("active");
      }
    }
  });
}

// Portfolio filtering functionality
const filterItems = document.querySelectorAll("[data-filter-item]");
const filterBtns = document.querySelectorAll("[data-filter-btn]");

let lastClickedFilterBtn = filterBtns[0]; // All button by default

for (let i = 0; i < filterBtns.length; i++) {
  filterBtns[i].addEventListener("click", function() {
    
    // Remove active class from last clicked filter button
    lastClickedFilterBtn.classList.remove("active");
    
    // Add active class to current clicked filter button
    this.classList.add("active");
    lastClickedFilterBtn = this;
    
    // Get the filter value
    const filterValue = this.textContent.toLowerCase().trim();
    
    for (let k = 0; k < filterItems.length; k++) {
      const itemCategory = filterItems[k].dataset.category.toLowerCase();
      
      // Show all items if "All" button is clicked
      if (filterValue === "all") {
        filterItems[k].classList.add("active");
      } 
      // Show items that match the clicked category
      else if (filterValue === itemCategory) {
        filterItems[k].classList.add("active");
      } 
      // Hide items that don't match the clicked category
      else {
        filterItems[k].classList.remove("active");
      }
    }
  });
}

// Handle form submissions
const form = document.querySelector('[data-form]');
const formInputs = document.querySelectorAll('[data-form-input]');
const formBtn = document.querySelector('[data-form-btn]');

// Enable form button when all inputs have value
for (let i = 0; i < formInputs.length; i++) {
  formInputs[i].addEventListener("input", function () {
    // Check all inputs have value
    let allInputsFilled = true;
    
    for (let j = 0; j < formInputs.length; j++) {
      if (formInputs[j].value === "") {
        allInputsFilled = false;
        break;
      }
    }
    
    // Enable/disable button based on inputs
    if (allInputsFilled) {
      formBtn.removeAttribute("disabled");
    } else {
      formBtn.setAttribute("disabled", "");
    }
  });
}

// Handle form submit
if (form) {
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    // Here you would typically add form submission logic
    // For now, just reset the form and disable the button
    form.reset();
    formBtn.setAttribute("disabled", "");
    alert("Your message has been sent successfully!");
  });
}

// Initialize - show first tab by default
// This ensures the "About" section is active on page load
window.addEventListener("load", function() {
  // Activate the first navigation link
  navigationLinks[0].classList.add("active");
  
  // Show the first page (About)
  for (let i = 0; i < pages.length; i++) {
    if (pages[i].dataset.page === "acerca") {
      pages[i].classList.add("active");
    } else {
      pages[i].classList.remove("active");
    }
  }
});