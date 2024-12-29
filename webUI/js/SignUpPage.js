
var passID="";
var emailAddress="";
var setPassword="";
var checkPassword="";

function getData(){
  passID=document.getElementById('passID').value;
  emailAddress=document.getElementById('email-address').value;
  setPassword=document.getElementById('set-password').value;
  checkPassword=document.getElementById('check-password').value;
  print();
}

function print(){
  var msg=document.createElement('div');
  msg.setAttribute("class","lable");
  msg.textContent=passID+";"+emailAddress+";"+setPassword+";"+checkPassword;
  document.getElementById('output').appendChild(msg);
}