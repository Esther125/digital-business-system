var passID="";
var emailAddress="";
var setPassword="";
var checkPassword="";

function getData(){
  passID=document.getElementById('passID').value;
  emailAddress=document.getElementById('email-address').value;
  setPassword=document.getElementById('set-password').value;
  checkPassword=document.getElementById('check-password').value;
  console.log(passID+";"+emailAddress+";"+setPassword+";"+checkPassword);
}