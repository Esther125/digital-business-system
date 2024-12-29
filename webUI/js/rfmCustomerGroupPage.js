var AWS = require("aws-sdk");

AWS.config.update({
    region: "ap-northeast-1"
});

var docClient = new AWS.DynamoDB.DocumentClient();

var table = "sysdata";

var params = {
    TableName: table,
    Key:{
        "accountType": "customer"
    }
};

var result="";

docClient.get(params, function(err, data) {
    if (err) {
    result="Unable to read item. Error JSON:"+ JSON.stringify(err, null, 2);
    } else {
    result="GetItem succeeded:"+ data;  
    }
});

function output(){
    var newRow=document.createElement('tr');
    var tdU=document.createElement('td');
    var tdR=document.createElement('td');
    var tdF=document.createElement('td');
    var tdM=document.createElement('td');
    var tdRFM=document.createElement('td');

    tdU.textContent=result;
    tdR.textContent="20240930";
    tdF.textContent="0";
    tdM.textContent="0";
    tdRFM.textContent="455";

    newRow.appendChild(tdU);
    newRow.appendChild(tdR);
    newRow.appendChild(tdF);
    newRow.appendChild(tdM);
    newRow.appendChild(tdRFM);

    document.getElementById('output').appendChild(newRow);
}
