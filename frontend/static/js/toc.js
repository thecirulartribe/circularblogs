document.addEventListener("DOMContentLoaded", () => {
  const blogContent = document.getElementById("blogcontent");
  const toc = document.getElementById("toc");
  const headers = blogContent.querySelectorAll("h2");

  if (headers.length) {
    const ul = document.createElement("ul");

    headers.forEach((header, index) => {
      const id = `section-${index}`;
      header.id = id;

      const li = document.createElement("li");
      const a = document.createElement("a");
      a.href = `#${id}`;
      a.textContent = header.textContent;

      li.appendChild(a);
      ul.appendChild(li);
    });

    toc.appendChild(ul);
  }
});
