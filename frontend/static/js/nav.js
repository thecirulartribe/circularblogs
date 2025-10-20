var openid = document.getElementById("open");
var closeid = document.getElementById("close");
var navid = document.getElementById("navigation");
var Sub = document.getElementById("subscribing");
var popup = document.getElementById("Popupclose");

function opennav() {
    openid.classList.add("navhide");
    closeid.classList.remove("navhide");
    navid.classList.add("navshow");
}

function closenav() {
    closeid.classList.add("navhide");
    openid.classList.remove("navhide");
    navid.classList.remove("navshow");
}

function closeform() {
    Sub.classList.add("hide");
}

function openform() {
    Sub.classList.remove("hide");
}

function closepopup() {
    popup.classList.add("hide");
    location.replace(location.href);
}

// Dropdown functionality
function toggleDropdown(event) {
    event.preventDefault();
    const dropdown = event.target.closest('.dropdown');
    const isActive = dropdown.classList.contains('active');

    // Close all other dropdowns
    document.querySelectorAll('.dropdown.active').forEach(d => {
        if (d !== dropdown) {
            d.classList.remove('active');
        }
    });

    // Toggle current dropdown
    if (isActive) {
        dropdown.classList.remove('active');
    } else {
        dropdown.classList.add('active');
    }
}

// Close dropdown when clicking outside
document.addEventListener('click', function (event) {
    if (!event.target.closest('.dropdown')) {
        document.querySelectorAll('.dropdown.active').forEach(dropdown => {
            dropdown.classList.remove('active');
        });
    }
});

// Close dropdown when pressing Escape key
document.addEventListener('keydown', function (event) {
    if (event.key === 'Escape') {
        document.querySelectorAll('.dropdown.active').forEach(dropdown => {
            dropdown.classList.remove('active');
        });
    }
});
