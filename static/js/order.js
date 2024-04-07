const stars = document.querySelectorAll(".rating input");
let test = document.getElementById("test");
let star1 = document.getElementById("star1");
star1.checked = true;
stars.forEach((star) => {
  star.addEventListener("click", function () {
    // Uncheck all stars
    stars.forEach((s) => (s.checked = false));

    // Check the clicked star
    this.checked = true;

    // Log the number of active stars and the selected rating
    const activeStars = document.querySelectorAll(".rating input:checked");
    const count = activeStars.length;
    const value = this.value;
    test.value = value;
  });
});
