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
    subject:  `A Quick Status Update`,
    text: `
Hello ${d["Name"]},

To give you an update on how you are doing in class, you are currently on track to move forward to the next module.

As you know, Moringa School looks at 3 major aspects of your learning in considering whether you proceed to the next module:
Attendance and punctuality.
Completion and quality of your IPs.
Positive contributions to the classroom environment; are you working well with others, and interpersonal skills.

As it stands:
Your attendance out of 100 is ${d["Attendance"]}.

As for your IPs:
IP1 out of 22 you have ${d["IP1 /31"]}.
IP2 out of 31 you have ${d["IP2 /28"]}.
IP3 out of 100% you have ${d["IP3 /100%"]}.

Based on the above scores we recommend that you spend the rest of the module working on keeping up with your attendance, IP submissions and quality, and your interpersonal dynamics. Your work has been good so far, and we want to encourage you to keep the momentum going.

This is an automatic email. Please do not reply to it. Follow up with your TM if you have any questions and fill out this form.
    
Best,
-Classroom Team
    `
  };
  transporter.sendMail(mailOptions, function(error, info){
    if (error) {
      console.log(error);
    } else {
      console.log('Email sent: ' + info.response);
    }
  });
  
}



csv().fromFile('data.csv').then((j)=>{
    const data=j
    for (i=0; i<data.length;i++){
      sendMail(data[i])
    }
})