// Table of Contents Generation
function generateTOC() {
  document.addEventListener('DOMContentLoaded', function () {
    // Small delay to ensure this runs after any legacy TOC scripts
    setTimeout(function() {
      try {
        const tocContent = document.querySelector('.toc-content');
        const contentWrapper = document.querySelector('.content-wrapper');

        if (tocContent && contentWrapper) {
          // Clear any existing content first to prevent duplication
          tocContent.innerHTML = '';

          const headings = contentWrapper.querySelectorAll('h1, h2, h3, h4, h5, h6');

          if (headings.length > 0) {
            const tocList = document.createElement('ul');

            headings.forEach((heading, index) => {
              // Create unique ID for heading if it doesn't exist
              if (!heading.id) {
                const id = `heading-${index}`;
                heading.id = id;
              }

              // Create TOC item
              const listItem = document.createElement('li');
              const link = document.createElement('a');
              link.href = `#${heading.id}`;
              link.textContent = heading.textContent;
              link.style.paddingLeft = `${(parseInt(heading.tagName.charAt(1)) - 1) * 12}px`;

              // Smooth scroll behavior
              link.addEventListener('click', function (e) {
                e.preventDefault();
                heading.scrollIntoView({
                  behavior: 'smooth',
                  block: 'start'
                });
              });

              listItem.appendChild(link);
              tocList.appendChild(listItem);
            });

            tocContent.appendChild(tocList);
          } else {
            // Hide TOC if no headings
            const tocSidebar = document.querySelector('.toc-sidebar');
            if (tocSidebar) {
              tocSidebar.style.display = 'none';
            }
          }
        }
      } catch (error) {
        console.warn('TOC generation failed:', error);
        // Hide TOC on error
        const tocSidebar = document.querySelector('.toc-sidebar');
        if (tocSidebar) {
          tocSidebar.style.display = 'none';
        }
      }
    }, 100); // Small delay to ensure this runs after legacy scripts
  });
}

// TOC Toggle Function (global)
window.toggleTOC = function() {
  try {
    const tocSidebar = document.querySelector('.toc-sidebar');
    const tocContent = document.getElementById('tocContent');

    if (tocSidebar && tocContent) {
      if (tocSidebar.classList.contains('toc-collapsed')) {
        tocSidebar.classList.remove('toc-collapsed');
        tocContent.style.display = 'block';
      } else {
        tocSidebar.classList.add('toc-collapsed');
        tocContent.style.display = 'none';
      }
    }
  } catch (error) {
    console.warn('TOC toggle failed:', error);
  }
}

generateTOC();
