
var emailAddress="";
var password="";

function getData(){
  emailAddress=document.getElementById('email-address').value;
  password=document.getElementById('password').value;
  print();
}

function print(){
  var msg=document.createElement('div');
  msg.setAttribute("class","label");
  msg.textContent=emailAddress+";"+password;
  document.getElementById('output').appendChild(msg);
}