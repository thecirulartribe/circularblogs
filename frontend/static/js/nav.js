var openid = document.getElementById("open");
var closeid = document.getElementById("close");
var navid = document.getElementById("navigation");
var mainid = document.getElementById("main");
var Sub = document.getElementById("subscribing");
function opennav() {
    openid.classList.add("navhide");
    closeid.classList.remove("navhide");
    navid.classList.add("navshow");
    mainid.classList.add("navshown");
    mainid.classList.add("mainshift");
};
function closenav() {
    closeid.classList.add("navhide");
    openid.classList.remove("navhide");
    navid.classList.remove("navshow");
    mainid.classList.remove("navshown");
    mainid.classList.remove("mainshift");
};
function closeform(){
    Sub.classList.add("hide");
};
function openform(){
    Sub.classList.remove("hide");
}