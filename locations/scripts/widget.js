var url = "{url}";
function httpGet(theUrl) {
  var xmlHttp = new XMLHttpRequest();
  xmlHttp.open("GET", theUrl, false);
  xmlHttp.send(null);
  return xmlHttp.responseText;
}
window.onload = function () {
  var el = document.getElementById('civil-widget');
  el.innerHTML = httpGet(url);
  el.style.width = '{width}px';
};
