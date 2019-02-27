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
    //Check for yes or no on recommendation
 
  //email options
  var mailOptions = {
    from: authEmail.user,
    to: d["Emails"],
    cc: ['andrew.anampiu@moringaschool.com','sam.ngigi@moringaschool.com','boluwaji.oyewumi@moringaschool.com '],
    subject:  `A Quick Status Update`,
    text: `
Hello ${d["First Name"]} ${d["Second Name"]},

This email serves to give you an update on how you are doing in class, ahead of movement to the intermediate track.
    
As it stands:
    Your attendance out of 100 is ${d["Attendance (%)"]}.
    
Assignment completion:
    Out of 100% you have ${d["Assigment Completion (%)"]}

As for your IPs:
    IP1 out of 100% you have ${d["Independent Project 1: Safaricom Landing page (%)"]}.
    IP2 out of 100% you have ${d["Independent Project 2: Marco Polo (%)"]}.

More information will be incoming about the intermediate and advanced tracks.
    
This is an automatic email. Please do not reply to it. Follow up with your TM if you have any questions.

Best,
-Classroom Team.
    
    `
  };
  //Error logging
  transporter.sendMail(mailOptions, function(error, info){
    if (error) {
      console.log(error,mailOptions["to"]);
    } else {
      console.log('Email sent: ' + info.response,mailOptions["to"]);
    }
  });
  
}

//Read from CSV and send emails
csv().fromFile('data.csv').then((j)=>{
    const data=j
    for (i=0; i<data.length;i++){
      sendMail(data[i])
    }
})