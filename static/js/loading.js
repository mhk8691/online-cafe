document.addEventListener("DOMContentLoaded", function () {
  setTimeout(function () {
    const loading = document.querySelector(".loader");
    const loading2 = document.querySelector(".bg");
    const loading3 = document.querySelector(".h3");
    loading.remove();
    loading2.remove();
    loading3.remove();
  }, 1000);
});
