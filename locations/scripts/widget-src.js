(function () {

"use strict";

var divID = "{div_id}";
var url = "{url}";
var width = "{width}px";

function httpGet(url, fn) {
  var xhr = new XMLHttpRequest();
  xhr.open("GET", url, true);
  xhr.onload = function (e) {
    if (xhr.readyState === 4) {
      if (xhr.status === 200) {
        fn.call(null, xhr.responseText);
      }
    }
  };
  xhr.send(null);
}

window.addEventListener('load', function () {
  var el = document.getElementById(divID);
  httpGet(url, function (response) {
    el.innerHTML = response;
  });
  el.style.width = width;
});

})();
