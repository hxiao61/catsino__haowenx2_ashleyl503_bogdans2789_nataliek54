function getRndInteger(min, max) {
  return Math.floor(Math.random() * (max - min)) + min;
}

const confettiContainer = document.getElementById("confetti");

// Confetti logic
function launchConfetti() {
  const confettiColors = [
    "#ffeb3b",
    "#ff5722",
    "#e91e63",
    "#00e676",
    "#03a9f4"
  ];

  for (let i = 0; i < 100; i++) {
    const confettiPiece = document.createElement("div");
    confettiPiece.classList.add("confetti-piece");
    confettiPiece.style.left = `${Math.random() * 100}vw`;
    confettiPiece.style.backgroundColor =
    confettiColors[Math.floor(Math.random() * confettiColors.length)];
    confettiPiece.style.animationDuration = `${Math.random() * 3 + 2}s`;
    confettiContainer.appendChild(confettiPiece);

  }
}

function clearConfetti() {
  while (confettiContainer.firstChild) {
    confettiContainer.removeChild(confettiContainer.firstChild);
  }
}

async function updateBalance(increment, won) {
  const response = await fetch("/addtuna?num="+increment + "&win=" + won, {method: 'POST'});
  if (response.ok) {
    const data = await response.json();
    const newBalance = data[0]
    document.getElementById('balance').innerText = newBalance;
  }
}

function result(msg) {
    document.getElementById('message').innerText = msg;
}

//BETTING ON TYPE FUNCTIONS
function one() { //bet on 1 - 18
  let x = getRndInteger(0, 36);
  // console.log(x);
  // console.log(1 <= x && x <= 18);
  if (1 <= x && x<= 18) {
    updateBalance(50, true);
    result('CONGRATULATIONS YOU WIN!!!');
  } else {
    updateBalance(-100, false);
    result('YOU LOST');
  }
}

function two() { //bet on even
  let x = getRndInteger(0, 36);
  // console.log(x);
  // console.log(x % 2 == 0);
  if (x % 2 == 0) {
    updateBalance(50, true);
    result('CONGRATULATIONS YOU WIN!!!');
  } else {
    updateBalance(-100, false);
    result('YOU LOST');
  }
}

function three() { //bet on red
  let x = getRndInteger(0, 36);
  // console.log(x);
  // console.log(x == 3 || x == 9 || x == 12 || x == 18 || x == 21 || x == 27 || x == 30||
  //             x == 36 || x == 5 || x == 14 || x == 23 || x == 32 || x == 1 || x == 7 ||
  //             x == 16 || x == 19 || x == 25 || x == 34);
  if (x == 3 || x == 9 || x == 12 || x == 18 || x == 21 || x == 27 || x == 30||
      x == 36 || x == 5 || x == 14 || x == 23 || x == 32 || x == 1 || x == 7 ||
      x == 16 || x == 19 || x == 25 || x == 34) {
    updateBalance(100, true);
    result('CONGRATULATIONS YOU WIN!!!');
  } else {
    updateBalance(-100, false);
    result('YOU LOST');
  }
}

function four() { //bet on black
  let x = getRndInteger(0, 36);
  // console.log(x);
  // console.log(x == 6 || x == 15 || x == 24 || x == 33 || x == 2 || x == 8 || x == 11||
  //     x == 17 || x == 20 || x == 26 || x == 29 || x == 35 || x == 4 || x == 10 ||
  //     x == 13 || x == 22 || x == 28 || x == 31);
  if (x == 6 || x == 15 || x == 24 || x == 33 || x == 2 || x == 8 || x == 11||
      x == 17 || x == 20 || x == 26 || x == 29 || x == 35 || x == 4 || x == 10 ||
      x == 13 || x == 22 || x == 28 || x == 31) {
    updateBalance(50, true);
    result('CONGRATULATIONS YOU WIN!!!');
  } else {
    updateBalance(-100, false);
    result('YOU LOST');
  }
}

function five() { //bet on odd
  let x = getRndInteger(0, 36);
  // console.log(x);
  // console.log(x % 2 != 0);
  if (x % 2 != 0) {
    updateBalance(50, true);
    result('CONGRATULATIONS YOU WIN!!!');
  } else {
    updateBalance(-100, false);
    result('YOU LOST');
  }
}

function six() { //bet on 19 - 36
  let x = getRndInteger(0, 36);
  // console.log(x);
  // console.log(19 <= x && x <= 36);
  if (19 <= x && x<= 36) {
    updateBalance(50, true);
    result('CONGRATULATIONS YOU WIN!!!');
  } else {
    updateBalance(-100, false);
    result('YOU LOST');
  }
}


//BETTING ON VALUE FUNCTIONS
function n0() {
  let x = getRndInteger(0, 36);
  console.log(x);
  if (x == 0) {
    updateBalance(200, true);
    result('CONGRATULATIONS YOU WIN!!!');
  } else {
    updateBalance(-100, false);
    result('YOU LOST');
  }
}

function n1() {
  let x = getRndInteger(0, 36);
  console.log(x);
  if (x == 1) {
    updateBalance(200, true);
    result('CONGRATULATIONS YOU WIN!!!');
  } else {
    updateBalance(-100, false);
    result('YOU LOST');
  }
}

function n2() {
  let x = getRndInteger(0, 36);
  console.log(x);
  if (x == 2) {
    updateBalance(200, true);
    result('CONGRATULATIONS YOU WIN!!!');
  } else {
    updateBalance(-100, false);
    result('YOU LOST');
  }
}

function n3() {
  let x = getRndInteger(0, 36);
  console.log(x);
  if (x == 3) {
    updateBalance(200, true);
    result('CONGRATULATIONS YOU WIN!!!');
  } else {
    updateBalance(-100, false);
    result('YOU LOST');
  }
}

function n4() {
  let x = getRndInteger(0, 36);
  console.log(x);
  if (x == 4) {
    updateBalance(200, true);
    result('CONGRATULATIONS YOU WIN!!!');
  } else {
    updateBalance(-100, false);
    result('YOU LOST');
  }
}

function n5() {
  let x = getRndInteger(0, 36);
  console.log(x);
  if (x == 5) {
    updateBalance(200, true);
    result('CONGRATULATIONS YOU WIN!!!');
  } else {
    updateBalance(-100, false);
    result('YOU LOST');
  }
}

function n6() {
  let x = getRndInteger(0, 36);
  console.log(x);
  if (x == 6) {
    updateBalance(200, true);
    result('CONGRATULATIONS YOU WIN!!!');
  } else {
    updateBalance(-100, false);
    result('YOU LOST');
  }
}

function n7() {
  let x = getRndInteger(0, 36);
  console.log(x);
  if (x == 7) {
    updateBalance(200, true);
    result('CONGRATULATIONS YOU WIN!!!');
  } else {
    updateBalance(-100, false);
    result('YOU LOST');
  }
}

function n8() {
  let x = getRndInteger(0, 36);
  console.log(x);
  if (x == 8) {
    updateBalance(200, true);
    result('CONGRATULATIONS YOU WIN!!!');
  } else {
    updateBalance(-100, false);
    result('YOU LOST');
  }
}

function n9() {
  let x = getRndInteger(0, 36);
  console.log(x);
  if (x == 9) {
    updateBalance(200, true);
    result('CONGRATULATIONS YOU WIN!!!');
  } else {
    updateBalance(-100, false);
    result('YOU LOST');
  }
}

function n10() {
  let x = getRndInteger(0, 36);
  console.log(x);
  if (x == 10) {
    updateBalance(200, true);
    result('CONGRATULATIONS YOU WIN!!!');
  } else {
    updateBalance(-100, false);
    result('YOU LOST');
  }
}

function n11() {
  let x = getRndInteger(0, 36);
  console.log(x);
  if (x == 11) {
    updateBalance(200, true);
    result('CONGRATULATIONS YOU WIN!!!');
  } else {
    updateBalance(-100, false);
    result('YOU LOST');
  }
}

function n12() {
  let x = getRndInteger(0, 36);
  console.log(x);
  if (x == 12) {
    updateBalance(200, true);
    result('CONGRATULATIONS YOU WIN!!!');
  } else {
    updateBalance(-100, false);
    result('YOU LOST');
  }
}

function n13() {
  let x = getRndInteger(0, 36);
  console.log(x);
  if (x == 13) {
    updateBalance(200, true);
    result('CONGRATULATIONS YOU WIN!!!');
  } else {
    updateBalance(-100, false);
    result('YOU LOST');
  }
}

function n14() {
  let x = getRndInteger(0, 36);
  console.log(x);
  if (x == 14) {
    updateBalance(200, true);
    result('CONGRATULATIONS YOU WIN!!!');
  } else {
    updateBalance(-100, false);
    result('YOU LOST');
  }
}

function n15() {
  let x = getRndInteger(0, 36);
  console.log(x);
  if (x == 15) {
    updateBalance(200, true);
    result('CONGRATULATIONS YOU WIN!!!');
  } else {
    updateBalance(-100, false);
    result('YOU LOST');
  }
}

function n16() {
  let x = getRndInteger(0, 36);
  console.log(x);
  if (x == 16) {
    updateBalance(200, true);
    result('CONGRATULATIONS YOU WIN!!!');
  } else {
    updateBalance(-100, false);
    result('YOU LOST');
  }
}

function n17() {
  let x = getRndInteger(0, 36);
  console.log(x);
  if (x == 17) {
    updateBalance(200, true);
    result('CONGRATULATIONS YOU WIN!!!');
  } else {
    updateBalance(-100, false);
    result('YOU LOST');
  }
}

function n18() {
  let x = getRndInteger(0, 36);
  console.log(x);
  if (x == 18) {
    updateBalance(200, true);
    result('CONGRATULATIONS YOU WIN!!!');
  } else {
    updateBalance(-100, false);
    result('YOU LOST');
  }
}

function n19() {
  let x = getRndInteger(0, 36);
  console.log(x);
  if (x == 19) {
    updateBalance(200, true);
    result('CONGRATULATIONS YOU WIN!!!');
  } else {
    updateBalance(-100, false);
    result('YOU LOST');
  }
}

function n20() {
  let x = getRndInteger(0, 36);
  console.log(x);
  if (x == 20) {
    updateBalance(200, true);
    result('CONGRATULATIONS YOU WIN!!!');
  } else {
    updateBalance(-100, false);
    result('YOU LOST');
  }
}

function n21() {
  let x = getRndInteger(0, 36);
  console.log(x);
  if (x == 21) {
    updateBalance(200, true);
    result('CONGRATULATIONS YOU WIN!!!');
  } else {
    updateBalance(-100, false);
    result('YOU LOST');
  }
}

function n22() {
  let x = getRndInteger(0, 36);
  console.log(x);
  if (x == 22) {
    updateBalance(200, true);
    result('CONGRATULATIONS YOU WIN!!!');
  } else {
    updateBalance(-100, false);
    result('YOU LOST');
  }
}

function n23() {
  let x = getRndInteger(0, 36);
  console.log(x);
  if (x == 23) {
    updateBalance(200, true);
    result('CONGRATULATIONS YOU WIN!!!');
  } else {
    updateBalance(-100, false);
    result('YOU LOST');
  }
}

function n24() {
  let x = getRndInteger(0, 36);
  console.log(x);
  if (x == 24) {
    updateBalance(200, true);
    result('CONGRATULATIONS YOU WIN!!!');
  } else {
    updateBalance(-100, false);
    result('YOU LOST');
  }
}

function n25() {
  let x = getRndInteger(0, 36);
  console.log(x);
  if (x == 25) {
    updateBalance(200, true);
    result('CONGRATULATIONS YOU WIN!!!');
  } else {
    updateBalance(-100, false);
    result('YOU LOST');
  }
}

function n26() {
  let x = getRndInteger(0, 36);
  console.log(x);
  if (x == 26) {
    updateBalance(200, true);
    result('CONGRATULATIONS YOU WIN!!!');
  } else {
    updateBalance(-100, false);
    result('YOU LOST');
  }
}

function n27() {
  let x = getRndInteger(0, 36);
  console.log(x);
  if (x == 27) {
    updateBalance(200, true);
    result('CONGRATULATIONS YOU WIN!!!');
  } else {
    updateBalance(-100, false);
    result('YOU LOST');
  }
}

function n28() {
  let x = getRndInteger(0, 36);
  console.log(x);
  if (x == 28) {
    updateBalance(200, true);
    result('CONGRATULATIONS YOU WIN!!!');
  } else {
    updateBalance(-100, false);
    result('YOU LOST');
  }
}

function n29() {
  let x = getRndInteger(0, 36);
  console.log(x);
  if (x == 29) {
    updateBalance(200, true);
    result('CONGRATULATIONS YOU WIN!!!');
  } else {
    updateBalance(-100, false);
    result('YOU LOST');
  }
}

function n30() {
  let x = getRndInteger(0, 36);
  console.log(x);
  if (x == 30) {
    updateBalance(200, true);
    result('CONGRATULATIONS YOU WIN!!!');
  } else {
    updateBalance(-100, false);
    result('YOU LOST');
  }
}

function n31() {
  let x = getRndInteger(0, 36);
  console.log(x);
  if (x == 31) {
    updateBalance(200, true);
    result('CONGRATULATIONS YOU WIN!!!');
  } else {
    updateBalance(-100, false);
    result('YOU LOST');
  }
}

function n32() {
  let x = getRndInteger(0, 36);
  console.log(x);
  if (x == 32) {
    updateBalance(200, true);
    result('CONGRATULATIONS YOU WIN!!!');
  } else {
    updateBalance(-100, false);
    result('YOU LOST');
  }
}

function n33() {
  let x = getRndInteger(0, 36);
  console.log(x);
  if (x == 33) {
    updateBalance(200, true);
    result('CONGRATULATIONS YOU WIN!!!');
  } else {
    updateBalance(-100, false);
    result('YOU LOST');
  }
}

function n34() {
  let x = getRndInteger(0, 36);
  console.log(x);
  if (x == 34) {
    updateBalance(200, true);
    result('CONGRATULATIONS YOU WIN!!!');
  } else {
    updateBalance(-100, false);
    result('YOU LOST');
  }
}

function n35() {
  let x = getRndInteger(0, 36);
  console.log(x);
  if (x == 35) {
    updateBalance(200, true);
    result('CONGRATULATIONS YOU WIN!!!');
  } else {
    updateBalance(-100, false);
    result('YOU LOST');
  }
}

function n36() {
  let x = getRndInteger(0, 36);
  console.log(x);
  if (x == 36) {
    updateBalance(200, true);
    result('CONGRATULATIONS YOU WIN!!!');
  } else {
    updateBalance(-100, false);
    result('YOU LOST');
  }
}