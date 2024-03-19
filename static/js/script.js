const increaseBtn = document.querySelector(".increaseBtn");
const decreaseBtn = document.querySelector(".decreaseBtn");
const numberInput = document.querySelector(".numberInput");

// تعریف تابعی برای افزایش مقدار
function increaseNumber() {
  let currentValue = parseInt(numberInput.value);
  numberInput.value = currentValue + 1;
}

// تعریف تابعی برای کاهش مقدار
function decreaseNumber() {
  let currentValue = parseInt(numberInput.value);
  numberInput.value = 0;
}

// اتصال توابع به دکمه‌ها
increaseBtn.addEventListener("click", increaseNumber);
decreaseBtn.addEventListener("click", decreaseNumber);
