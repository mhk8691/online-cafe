window.addEventListener("scroll", function () {
  const content = document.querySelector(".content");
  const contentPosition = content.getBoundingClientRect().top;
  const screenHeight = window.innerHeight / 1.5; // تعداد موردنیاز برای شروع انیمیشن

  if (contentPosition < screenHeight) {
    content.classList.add("scrolling");
  }
});
