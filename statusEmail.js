const csv = require("csvtojson")
const fs = require("fs")
const nodemailer = require('nodemailer');
var smtpTransport = require('nodemailer-smtp-transport');
require('dotenv').config()

// this may be vulnearable to MITM attacks, remember to enable less-secure on google.
process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0'

const authEmail = {
  user: process.env.EMAIL_USER,
  pass: process.env.EMAIL_PASSWORD,
}

var transporter = nodemailer.createTransport(smtpTransport({
  service: 'gmail',
  auth: authEmail
}))

//Different emails sent for different criteria

var notOnTrack = `

`


var sendMail = function (d) {
  //Check for yes or no on recommendation
  if (d['First Recommendation'] === 'Yes') {
    text = `
Hello ${d["Name"]}

To give you an update on how you are doing in class, you are currently on track to move forward to the next module.
    
As you know, Moringa School looks at 3 major aspects of your learning in considering whether you proceed to the next module:
  Attendance and punctuality.
  Completion and quality of your IPs.
  Positive contributions to the classroom environment; are you working well with others, and interpersonal skills.
    
As it stands:
  Your attendance out of 100 is ${d["Attendance /100"]}.
    
As for your IPs:
Angular
  IP1 out of 31 you have ${d["IP1 /31"]}.
  IP2 out of 28 you have ${d["IP2 /28"]}.
Python
  IP1 out of 21 you have ${d["IP3 /21"]}.
  IP2 out of 22 you have ${d["IP4 /22"]}.
    
Based on the above scores we recommend that you spend the rest of the module working on keeping up with your attendance, IP submissions and quality, and your interpersonal dynamics. Your work has been good so far, and we want to encourage you to keep the momentum going.
    
This is an automatic email. Please do not reply to it. Follow up with your TM if you have any questions and fill out this form.
https://goo.gl/forms/0IirlKjvqZ7Qwyt72

Best,
-Classroom Team.
      `;
  } else {
    text = `
Hello ${d["Name"]}

To give you an update on how you are doing in class, you are currently not on track to move forward to the next module but have an opportunity to improve before final decisions are made. Please continue reading to understand why this is, and how you can improve.

As you know, Moringa School looks at 3 major aspects of your learning in considering whether you proceed to the next module:
  Attendance and punctuality.
  Completion and quality of your IPs.
  Positive contributions to the classroom environment; are you working well with others, and interpersonal skills.
    
As it stands:
  Your attendance out of 100 is ${d["Attendance /100"]}.

As for your IPs:
Angular
  IP1 out of 31 you have ${d["IP1 /31"]}.
  IP2 out of 28 you have ${d["IP2 /28"]}.
Python
  IP1 out of 21 you have ${d["IP3 /21"]}.
  IP2 out of 22 you have ${d["IP4 /22"]}.
Based on the above scores we recommend that you spend the rest of the module working on improving your ${d["Reason(first recommendation)"]}.
   
This is an automatic email. Please do not reply to it. Follow up with your TM if you have any questions and fill out this form.
https://goo.gl/forms/0IirlKjvqZ7Qwyt72

Best,
-Classroom Team.
      `;
  }
  //email options
  var mailOptions = {
    from: authEmail.user,
    to: d["Email"],
    cc: ['newton.karanu@moringaschool.com'],
    subject: `A Quick Status Update`,
    text: text
  };
  //Error logging
  transporter.sendMail(mailOptions, function (error, info) {
    if (error) {
      console.log(error, mailOptions["to"]);
      var callback = function (err, res) {
        if (err) {
          throw err;
        }
        console.log(res)
      }
      var errFile = "./errors.log"
      var errorFile = fs.open("./errors.log", "r+", callback);
      today = "\n" + Date() + ":======================================================================= \n";
      if (errorFile != -1) {// If the file has been successfully opened


        fs.appendFile(errFile, error, callback); // Write the string to a file
        fs.appendFile(errFile, today, callback); // Write the string to a file
        // fs.close(errorFile, callback); // Close the file 
      }
      console.log("check the error files for more details")
    } else {
      console.log('Email sent: ' + info.response, mailOptions["to"]);
    }
  });

}

//Read from CSV and send emails
csv().fromFile('data.csv').then((j) => {
  const data = j
  for (i = 0; i < data.length; i++) {
    sendMail(data[i])
  }
})