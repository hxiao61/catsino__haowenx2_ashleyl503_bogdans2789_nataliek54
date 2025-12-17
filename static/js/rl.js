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

function one() { //1 - 18
  let x = getRndInteger(0, 36);
  console.log(x);
  console.log(1 <= x && x<= 18);
  if (1 <= x && x<= 18) {
    updateBalance(50, true);
  } else {
    updateBalance(-100, false);
  }
}

document.getElementById("one").addEventListener('click', () => {
  one();
});


function two() { //even
  let x = getRndInteger(0, 36);
  console.log(x);
  console.log(x % 2 == 0);
  if (x % 2 ==0) {
    updateBalance(50, true);
  }
}

document.getElementById("one").addEventListener('click', () => {
  one();
});
