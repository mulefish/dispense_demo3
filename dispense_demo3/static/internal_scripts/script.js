const prevButton = document.querySelector('.carousel-button.prev');
const nextButton = document.querySelector('.carousel-button.next');
const carouselContainer = document.querySelector('.carousel-container');
let currentIndex = 0;

prevButton.addEventListener('click', () => {
    console.log("prevButton")
    if (currentIndex > 0) {
        currentIndex--;
        updateCarousel();
    }
});

nextButton.addEventListener('click', () => {
    console.log("nextButton")
    if (currentIndex < carouselContainer.children.length - 1) {
        currentIndex++;
        updateCarousel();
    }
});

function updateCarousel() {
    console.log("updateCarousel")
    const translateX = -currentIndex * 100;
    carouselContainer.style.transform = `translateX(${translateX}%)`;
}
