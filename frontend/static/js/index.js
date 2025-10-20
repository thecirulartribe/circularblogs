let i = 0;
let placeholder = "";
const txt1 = "Enter what you want to know about?";
const txt2 = "Search for keywords";
const txt3 = "Search for blogs";
const speed = 50;
function search1() {
    placeholder += txt1.charAt(i);
    document.getElementById("search").setAttribute("placeholder", placeholder);
    i++;
    timer = setTimeout(search1, speed);
    if (i == 50) {
        clearTimeout(timer);
        i = 0;
        placeholder = "";
        search2();
    }
}
function search2() {
    placeholder += txt2.charAt(i);
    document.getElementById("search").setAttribute("placeholder", placeholder);
    i++;
    timer = setTimeout(search2, speed);
    if (i == 40) {
        clearTimeout(timer);
        i = 0;
        placeholder = "";
        search3();
    }
}
function search3() {
    placeholder += txt3.charAt(i);
    document.getElementById("search").setAttribute("placeholder", placeholder);
    i++;
    timer = setTimeout(search3, speed);
    if (i == 40) {
        clearTimeout(timer);
        i = 0;
        placeholder = "";
        search1();
    }
}
search1()
// Enhanced Categories Functionality
document.addEventListener('DOMContentLoaded', function () {
    const categoriesContainer = document.querySelector('.categories ul');
    const categoryLinks = document.querySelectorAll('.categories ul li a');

    // Add smooth scrolling for categories on mobile
    if (categoriesContainer) {
        let isScrolling = false;

        // Add scroll indicators
        function updateScrollIndicators() {
            const container = categoriesContainer.parentElement;
            const scrollLeft = categoriesContainer.scrollLeft;
            const maxScroll = categoriesContainer.scrollWidth - categoriesContainer.clientWidth;

            if (scrollLeft <= 10) {
                container.classList.add('scroll-start');
            } else {
                container.classList.remove('scroll-start');
            }

            if (scrollLeft >= maxScroll - 10) {
                container.classList.add('scroll-end');
            } else {
                container.classList.remove('scroll-end');
            }
        }

        categoriesContainer.addEventListener('scroll', function () {
            if (!isScrolling) {
                window.requestAnimationFrame(function () {
                    updateScrollIndicators();
                    isScrolling = false;
                });
                isScrolling = true;
            }
        });

        // Initial check
        updateScrollIndicators();

        // Smooth scroll to active category on page load
        const activeCategory = document.querySelector('.categories ul li a.active');
        if (activeCategory) {
            setTimeout(() => {
                activeCategory.scrollIntoView({
                    behavior: 'smooth',
                    block: 'nearest',
                    inline: 'center'
                });
            }, 100);
        }
    }

    // Add loading state when clicking category links
    categoryLinks.forEach(link => {
        link.addEventListener('click', function (e) {
            // Remove active class from all links
            categoryLinks.forEach(l => l.classList.remove('active'));

            // Add active class to clicked link
            this.classList.add('active');

            // Add loading state
            this.classList.add('loading');

            // Remove loading state after navigation (fallback)
            setTimeout(() => {
                this.classList.remove('loading');
            }, 2000);
        });
    });

    // Keyboard navigation for categories
    categoriesContainer?.addEventListener('keydown', function (e) {
        const focusedElement = document.activeElement;
        const categoryLinks = Array.from(this.querySelectorAll('a'));
        const currentIndex = categoryLinks.indexOf(focusedElement);

        if (e.key === 'ArrowRight' && currentIndex < categoryLinks.length - 1) {
            e.preventDefault();
            categoryLinks[currentIndex + 1].focus();
            categoryLinks[currentIndex + 1].scrollIntoView({
                behavior: 'smooth',
                block: 'nearest',
                inline: 'center'
            });
        } else if (e.key === 'ArrowLeft' && currentIndex > 0) {
            e.preventDefault();
            categoryLinks[currentIndex - 1].focus();
            categoryLinks[currentIndex - 1].scrollIntoView({
                behavior: 'smooth',
                block: 'nearest',
                inline: 'center'
            });
        }
    });

    // Add touch/swipe support for better mobile experience
    let startX = 0;
    let scrollLeft = 0;

    categoriesContainer?.addEventListener('touchstart', function (e) {
        startX = e.touches[0].pageX - this.offsetLeft;
        scrollLeft = this.scrollLeft;
    });

    categoriesContainer?.addEventListener('touchmove', function (e) {
        if (!startX) return;
        e.preventDefault();
        const x = e.touches[0].pageX - this.offsetLeft;
        const walk = (x - startX) * 2;
        this.scrollLeft = scrollLeft - walk;
    });

    categoriesContainer?.addEventListener('touchend', function () {
        startX = 0;
    });
});
