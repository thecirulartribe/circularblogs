var blogs = document.getElementsByClassName('content-wrapper')
const count = blogs[0].getElementsByTagName('a').length

function addRelAttributes(element, newAttributes) {
    let currentRel = element.getAttribute("rel") || "";
    let updatedRel = [...new Set(currentRel.split(" ").concat(newAttributes))].join(" ");
    element.setAttribute("rel", updatedRel);
};

function default_link () {
for (let i = 0; i< count ;i++ ){
  blogs[0].getElementsByTagName('a')[i].setAttribute("target","_blank")
  let anchor = blogs[0].getElementsByTagName('a')[i];
  addRelAttributes(anchor, ["noopener", "noreferrer", "nofollow"]);
};
};

function dofollow () {
for (let i = 0; i< count ;i++ ){
  blogs[0].getElementsByTagName('a')[i].setAttribute("target","_blank")
  let anchor = blogs[0].getElementsByTagName('a')[i];
  addRelAttributes(anchor, ["dofollow"]);
};
};

function nofollow() {
for (let i = 0; i< count ;i++ ){
  blogs[0].getElementsByTagName('a')[i].setAttribute("target","_blank")
  let anchor = blogs[0].getElementsByTagName('a')[i];
  addRelAttributes(anchor, ["nofollow"]);
};
};

function noopener() {
for (let i = 0; i< count ;i++ ){
  blogs[0].getElementsByTagName('a')[i].setAttribute("target","_blank")
  let anchor = blogs[0].getElementsByTagName('a')[i];
  addRelAttributes(anchor, ["noopener"]);
};
};

function noreferrer() {
for (let i = 0; i< count ;i++ ){
  blogs[0].getElementsByTagName('a')[i].setAttribute("target","_blank")
  let anchor = blogs[0].getElementsByTagName('a')[i];
  addRelAttributes(anchor, ["noreferrer"]);
};
};