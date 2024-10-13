let i = 0;
let placeholder = "";
const txt1 = "Enter what you want to know about?";
const txt2 = "Search for keywords";
const txt3 = "Search for blogs";
const speed = 50;
function search1(){
    placeholder += txt1.charAt(i);
    document.getElementById("search").setAttribute("placeholder",placeholder);
    i++;
    timer = setTimeout(search1,speed);
    if(i == 50){
        clearTimeout(timer);
        i = 0;
        placeholder = "";
        search2();
    }
}
function search2(){
    placeholder += txt2.charAt(i);
    document.getElementById("search").setAttribute("placeholder",placeholder);
    i++;
    timer = setTimeout(search2,speed);
    if(i == 40){
        clearTimeout(timer);
        i = 0;
        placeholder = "";
        search3();
    }
}
function search3(){
    placeholder += txt3.charAt(i);
    document.getElementById("search").setAttribute("placeholder",placeholder);
    i++;
    timer = setTimeout(search3,speed);
    if(i == 40){
        clearTimeout(timer);
        i = 0;
        placeholder = "";
        search1();
    }
}
search1()
function moreblog(){
    var moreblog = document.getElementById("moreblog");
    moreblog.style.display = "flex";
    document.getElementById("moretxt").style.display = "none";
}