"use strict";

const alertMsg = document.getElementById("alert-msg");
const title = document.getElementById("title");

$(document).ready(function () {
  const alertMsg = $("#alert-msg");
  if (alertMsg.length) {
    if (title) {
      title.style.margin = "0";
    }
    setTimeout(function () {
      alertMsg.fadeOut(700, function () {
        alertMsg.remove();
        if (title) {
          title.style.marginTop = "40px";
        }
      });
    }, 3000);
  }
});