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

const spinSound = new Audio("https://www.fesliyanstudios.com/play-mp3/387"); // Spin effect
const winSound = new Audio("https://www.fesliyanstudios.com/play-mp3/380"); // Win effect

handle.addEventListener("click", () => {
  if (isSpinning) return;
  isSpinning = true;

  clearConfetti();

  spinSound.play();

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

function checkResult() {
  const symbol1 = getSymbolAtStop(reels[0]);
  const symbol2 = getSymbolAtStop(reels[1]);
  const symbol3 = getSymbolAtStop(reels[2]);

  if (symbol1 === symbol2 && symbol2 === symbol3) {
    winSound.play();
    launchConfetti();
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
