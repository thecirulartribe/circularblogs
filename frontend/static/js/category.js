var urls = window.location.href;
urls = urls.split('/');
var current = urls.pop();
var current_tag = document.getElementById(current);
var categories = document.getElementById("categories")
var shift = document.getElementById(current).getBoundingClientRect();
var shift_by = shift.left;
categories.scrollLeft = shift_by - 100
var active_class = document.getElementsByClassName('active')[0].id;
var active_id = document.getElementById(active_class);
active_id.classList.remove('active');
current_tag.classList.add('active');
