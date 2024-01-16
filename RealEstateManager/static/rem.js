loadHTML('../todo_list', 'todos');
loadHTML('../apartment_list', 'content');

function loadHTML(source, target) {
  fetch(source)
      .then(response => response.text())
      .then(text => document.getElementById(target).innerHTML = text);
  console.log("Source loaded" + source);
}

function showToDo() {
//today's day (of month):
let date = new Date().getDate();
console.log(date);
}
showToDo()

function hideToDo() {
}