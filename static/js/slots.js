const reels = [
  document.getElementById("symbol-container1"),
  document.getElementById("symbol-container2"),
  document.getElementById("symbol-container3")
];

const handle = document.getElementById("handle");
const resultMessage = document.getElementById("resultMessage");
const confettiContainer = document.getElementById("confetti");

const symbols = ["😺", "😸", "😻", "🙀", "😼"];
const spinDuration = 500;
let isSpinning = false;
let lowBal = false;

const spinSound = new Audio('cha-ching.mp3'); // Spin effect
const winSound = new Audio("cha-ching.mp3");
const nonWinSound = new Audio("https://www.fesliyanstudios.com/play-mp3/5638"); //sad trombone



handle.addEventListener("click", () => {

  if (isSpinning) return;
  if (document.getElementById('balance').innerText < 50) {
    handle.disabled = true;
    console.log('a')
    return;
  }
  else {
    handle.disabled = false;
  }
  isSpinning = true;

  clearConfetti();

  spinSound.play();
  updateBalance(-50, false);

  // randomize
  reels.forEach((reel) => {
    const randomStop = Math.floor(Math.random() * symbols.length) * -100;
    reel.style.transition = "transform 0.5s cubic-bezier(0.23, 1, 0.32, 1)";
    reel.style.transform = `translateY(${randomStop}px)`;
  });

  // check
  setTimeout(() => {
    checkResult();
    isSpinning = false;
  }, spinDuration);
});

async function updateBalance(increment, won) {
  const response = await fetch("/addtuna?num="+increment + "&win=" + won, {method: 'POST'});
  if (response.ok) {
    const data = await response.json();
    const newBalance = data[0]
    document.getElementById('balance').innerText = newBalance;
  }
}

function checkResult() {
  const symbol1 = getSymbolAtStop(reels[0]);
  const symbol2 = getSymbolAtStop(reels[1]);
  const symbol3 = getSymbolAtStop(reels[2]);

  if (symbol1 === symbol2 && symbol2 === symbol3) {
    winSound.play();
    launchConfetti();
    updateBalance(2000, true);
  } else {
    resultMessage.textContent = "";
    resultMessage.classList.add("show-message");

  }
}

function getSymbolAtStop(reel) {
  const translateY = parseInt(
    reel.style.transform.replace("translateY(", "").replace("px)", "")
  );
  const symbolIndex = Math.abs(translateY / 100) % symbols.length;
  return symbols[symbolIndex];
}

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
