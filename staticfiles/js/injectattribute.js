var blogs = document.getElementsByClassName('content')
const count = blogs[0].getElementsByTagName('a').length
for (let i = 0; i< count ;i++ ){
  blogs[0].getElementsByTagName('a')[i].setAttribute("target","_blank")
  blogs[0].getElementsByTagName('a')[i].setAttribute("rel","noopener noreferrer");
};