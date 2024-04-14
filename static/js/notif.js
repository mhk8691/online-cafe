// import { get } from "axios";
let notification = document.getElementsByClassName("notification");
function notif() {
    
    for(let i = 0;i<=notification.length;i++){
        notification[i].style.visibility = "hidden"
    }
    
    

}
let not = document.getElementById("not");
if (notification.length == 0) {
  not.style.visibility = "hidden";
}