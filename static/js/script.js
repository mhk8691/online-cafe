// dark mode and light mode
document.getElementById("btnSwitch").addEventListener("click", () => {
  if (document.documentElement.getAttribute("data-bs-theme") == "dark") {
    document.documentElement.setAttribute("data-bs-theme", "light");
  } else {
    document.documentElement.setAttribute("data-bs-theme", "dark");
  }
});

var count = 1;
function setColor() {
  var property = document.getElementById("btnSwitch");
  if (count == 0) {
    
    property.innerHTML = "شب";
    count = 1;
  } else {
    

    property.innerHTML = "روز";

    count = 0;
  }
}
