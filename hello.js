// let i=0;
// for(let i=0;i<6;i++){
//     console.log("hello",i);
// }

// let j=24;
// console.log(j+i);
// console.log(process);
// console.log(process.env.PASSWORD);

// console.log("hello");


let variable = 0;

function cartcount() {
    variable = variable + 1;
    console.log(variable);
}

function reset(){
    variable=0;
    
}

function showquantity(){
    console.log(variable);
}

//   const score={
//         tie:0,
//         win:0,
//         loss:0,

//     }

// function rockpaper(input) {
//     const arr = ['rock', 'paper', 'scissor'];
  
//     // pick random choice for computer
//     const comp = arr[Math.floor(Math.random() * arr.length)];

//     if (input === comp) {
//         score.tie=score.tie+1;
//     alert( `You and computer predicted ${input}. It's a draw.`);
//            alert(score);
        
//     }
//     else if (input === 'scissor' && comp === 'paper') {
//         score.win=score.win+1;
//         console.log(`You chose ${input}, computer chose ${comp}. You won!,`);
//            console.log(score);
//     }
//     else if (input === 'rock' && comp === 'scissor') {
//         score.win=score.win+1;
//         console.log(`You chose ${input}, computer chose ${comp}. You won!,,`);
//            console.log(score);
//     }
//     else if (input === 'paper' && comp === 'rock') {
//         score.win=score.win+1;
//         console.log(`You chose ${input}, computer chose ${comp}. You won!,,`);
//            console.log(score);

//     }
//     else {
//         score.loss=score.loss+1;
//         console.log(`You chose ${input}, computer chose ${comp}. You lost!,,`);
//         console.log(score);
//     }
// }


const score = {
    tie: 0,
    win: 0,
    loss: 0,
};

function rockpaper(input) {
    const arr = ['rock', 'paper', 'scissor'];
    const comp = arr[Math.floor(Math.random() * arr.length)];

    let result = "";

    if (input === comp) {
        score.tie++;
        result = "DRAW";
    }
    else if (input === 'scissor' && comp === 'paper') {
        score.win++;
        result = "YOU WIN";
    }
    else if (input === 'rock' && comp === 'scissor') {
        score.win++;
        result = "YOU WIN";
    }
    else if (input === 'paper' && comp === 'rock') {
        score.win++;
        result = "YOU WIN";
    }
    else {
        score.loss++;
        result = "YOU LOSE";
    }

    // Single alert with everything
    alert(
        `Result: ${result}\n\n` +
        `You chose      : ${input}\n` +
        `Computer chose : ${comp}\n\n` +
        `Score:\n` +
        `Win  : ${score.win}\n` +
        `Loss : ${score.loss}\n` +
        `Tie  : ${score.tie}`
    );
}

function reset(){
    score.tie=0,
    score.win=0,
    score.loss=0;
    alert(
        `scores has been reset:\n
        wins:${score.win}\n
        loss:${score.loss}\n
        tie:${score.tie}`
    );
}


