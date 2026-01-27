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

function rockpaper(input) {
    const arr = ['rock', 'paper', 'scissor'];

    // pick random choice for computer
    const comp = arr[Math.floor(Math.random() * arr.length)];

    if (input === comp) {
        console.log(`You and computer predicted ${input}. It's a draw.`);
    }
    else if (input === 'scissor' && comp === 'paper') {
        console.log(`You chose ${input}, computer chose ${comp}. You won!`);
    }
    else if (input === 'rock' && comp === 'scissor') {
        console.log(`You chose ${input}, computer chose ${comp}. You won!`);
    }
    else if (input === 'paper' && comp === 'rock') {
        console.log(`You chose ${input}, computer chose ${comp}. You won!`);
    }
    else {
        console.log(`You chose ${input}, computer chose ${comp}. You lost!`);
    }
}
