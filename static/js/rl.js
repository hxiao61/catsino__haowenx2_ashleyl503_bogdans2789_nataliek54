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

function one() { //bet on 1 - 18
  let x = getRndInteger(0, 36);
  // console.log(x);
  // console.log(1 <= x && x <= 18);
  if (1 <= x && x<= 18) {
    updateBalance(50, true);
  } else {
    updateBalance(-100, false);
  }
}

function two() { //bet on even
  let x = getRndInteger(0, 36);
  // console.log(x);
  // console.log(x % 2 == 0);
  if (x % 2 == 0) {
    updateBalance(50, true);
  } else {
    updateBalance(-100, false);
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
    updateBalance(50, true);
  } else {
    updateBalance(-100, false);
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
  } else {
    updateBalance(-100, false);
  }
}

function five() { //bet on odd
  let x = getRndInteger(0, 36);
  // console.log(x);
  // console.log(x % 2 != 0);
  if (x % 2 != 0) {
    updateBalance(50, true);
  } else {
    updateBalance(-100, false);
  }
}

function six() { //bet on 19 - 36
  let x = getRndInteger(0, 36);
  // console.log(x);
  // console.log(19 <= x && x <= 36);
  if (19 <= x && x<= 36) {
    updateBalance(50, true);
  } else {
    updateBalance(-100, false);
  }
}
