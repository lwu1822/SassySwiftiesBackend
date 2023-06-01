var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http);

let correctAnswers = 0;
let incorrectAnswers = 0;
let usersCorrect = [];
let usersIncorrect = [];
let totalAnswers = 0;
let correctPercentage = 0;


// Return the teacher page
app.get('/admin', function(req, res){
  res.sendFile(__dirname + '/kahoot/admin.html');
});

// Return the student page
app.get('/game', function(req, res){
  res.sendFile(__dirname + '/kahoot/game.html');
});

// Initially correct answer is blank
var correctanswer = "";

// If we have a connection...
io.on('connection', function(socket){

  // If a question is submitted...
  socket.on('submitquestion', function(quesdata){

    // What is the question?  log it in console for debug...
    console.log("question submitted: " + JSON.stringify(quesdata) + " " + quesdata.question + " " + quesdata.questionType);
    // Set the correct answer
    correctanswer = quesdata.answer;
    // Broadcast question to all connections except sender, i.e. except teacher
    socket.broadcast.emit('deliverquestion', {question: quesdata.question, questionType: quesdata.questionType, timeLimit: quesdata.timeLimit});

  });

  // If an answer to the question is received...
  socket.on('answerquestion', function(answerdata) {
    // Send back the result, but only to the client that sent the answer
    
    if(answerdata.answer == correctanswer){
      correctAnswers++;
      usersCorrect.push(answerdata.username);
    } else {
      incorrectAnswers++;
      usersIncorrect.push(answerdata.username);
    }

    totalAnswers = correctAnswers + incorrectAnswers;
    correctAnswers = correctAnswers;
    incorrectAnswers = incorrectAnswers;
    incorrectUsers = usersIncorrect;
    correctUsers = usersCorrect;
    let percentage = (correctAnswers/totalAnswers)* 100;

    socket.broadcast.emit("deliverData",{totalAnswers:totalAnswers,correctAnswers:correctAnswers,incorrectAnswers:incorrectAnswers,incorrectUsers:incorrectUsers,correctUsers:correctUsers,percentage:percentage});

    
    io.to(socket.id).emit("resultquestion"
                         ,{correct: (correctanswer == answerdata.answer) 
                         ,answer: correctanswer
                        ,username:answerdata.username}
                         );          
    });
    
  
});

// Have the server listen...
http.listen(8000, function(){
  console.log('listening on *:8000');
});
