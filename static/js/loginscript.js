const loginButton = document.getElementById('loginButton')
const username = document.getElementById('username');
const password = document.getElementById('password');

loginButton.addEventListener('click', (event) => {
  if (username.value.trim() == ''){
    error(username)
  }
  else
    pass(username)
  if (password.value.trim() == ''){
    error(password)
  }
  else
    pass(password)
});

/*indicators*/
function error(element){
  element.style.border = '3px red solid';
  preventDefault();
}
function pass(element){
  element.style.border = '3px green solid';
}
