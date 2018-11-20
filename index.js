
const csv= require("csvtojson")
const nodemailer = require('nodemailer');
var smtpTransport = require('nodemailer-smtp-transport');
require('dotenv').config()

// this may be vulnearable to MITM attacks, remember to enable less-secure on google.
process.env.NODE_TLS_REJECT_UNAUTHORIZED='0'

const authEmail={
  user:process.env.EMAIL_USER,
  pass:process.env.EMAIL_PASSWORD,
}

var transporter = nodemailer.createTransport(smtpTransport({
  service: 'gmail',
  auth: authEmail
}))

var sendMail= function(d){
  var mailOptions = {
    from: authEmail.user,
    to: d["Email"],
    subject:  `Scores`,
    text: `Hi ${d["Name"]}, your score is ${d["Score"]}`
  };
  transporter.sendMail(mailOptions, function(error, info){
    if (error) {
      console.log(error);
    } else {
      console.log('Email sent: ' + info.response);
    }
  });
  
}



csv().fromFile('sample.csv').then((j)=>{
    const data=j
    for (i=0; i<data.length;i++){
      sendMail(data[i])
    }
})