let cards = [];
let deckId = "";
let bet = 0;

async function Setup()
{
  let idResponse = await fetch("https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1");
  let idData = await idResponse.json();
  deckId = idData.deck_id;

  let drawResponse = await fetch(`https://deckofcardsapi.com/api/deck/${deckId}/draw/?count=5`);
  let drawData = await drawResponse.json();

  cards.push(drawData.cards[0]);
  cards.push(drawData.cards[1]);
  cards.push(drawData.cards[2]);
  cards.push(drawData.cards[3]);
  cards.push(drawData.cards[4]);

  document.getElementById('cds').appendChild(document.createTextNode(cards[0].code + " "));
  document.getElementById('cds').appendChild(document.createTextNode(cards[1].code + " "));
  document.getElementById('cds').appendChild(document.createTextNode(cards[2].code + " "));
  document.getElementById('cds').appendChild(document.createTextNode(cards[3].code + " "));
  document.getElementById('cds').appendChild(document.createTextNode(cards[4].code));
  bet = document.getElementById('betOUT').value;
  HandConvert();
  CheckHand();
}


function HandConvert()
{
  for (let i = 0; i < cards.length; i++)
  {
    if (cards[i].value == "JACK") cards[i].value = "11";
    else if (cards[i].value == "QUEEN") cards[i].value = "12";
    else if (cards[i].value == "KING") cards[i].value = "13";
    else if (cards[i].value == "ACE") cards[i].value = "14";
  }
}

function CheckHand()
{
  let message = document.getElementById('msg');
  let hasHand = 0;
  let multiplier = 0;
  let handValues = [125, 25, 12.5, 4.5, 3, 2.5, 2, 1.5, 1];
  let handMsgs = ["royal flush", "straight flush", "four of a kind", "full house", "flush", "straight", "three of a kind", "two pair", "one pair"];
  let hands= [0, 0, 0, 0, 0, 0, 0, 0, 0];
  /*
  0 = royal flush           `
  1 = straight flush        `
  2 = four of a kind        `
  3 = full house            `
  4 = flush                 `
  5 = straight              `
  7 = three of a kind       `
  8 = two pair              `
  9 = one pair              `
  */

  cards.sort();

  //checking for ONE PAIRs, THREE OF A KIND and FOUR OF A KIND
  for (let i = 0; i < cards.length-2; i++)
  {
    if (cards[i].value == cards[i+1].value)
    {
      if (i<cards.length-4 && cards[i].value == cards[i+3].value && cards[i].value == cards[i+2].value)
      {
        hands[2]++;
        i+=3;
      }
      else if (i<cards.length-3 && cards[i].value == cards[i+2].value)
      {
        hands[7]++;
        i+=2;
      }
      else
      {
        hands[9]++;
        i++;
      }
    }
  }

  if (hands[9] == 2) //checking for TWO PAIR
    hands[8]++;
  if (hands[9] == 1 && hands[7] == 1) //checking for FULL HOUSE
    hands[3]++;

  if (parseInt(cards[4].value)==parseInt(cards[3].value)+1 && parseInt(cards[3].value)==parseInt(cards[2].value)+1 && parseInt(cards[2].value)==parseInt(cards[1].value)+1 && parseInt(cards[1].value)==parseInt(cards[0].value)+1) hands[5]++;
  else if (parseInt(cards[4].value)==13 && parseInt(cards[0].value)==2 && parseInt(cards[3].value)==parseInt(cards[2].value)+1 && parseInt(cards[2].value)==parseInt(cards[1].value)+1 && parseInt(cards[1].value)==parseInt(cards[0].value)+1) hands[5]++;
  //checks for straight

  if (cards[0].suit.localeCompare(cards[1].suit)==0 && cards[0].suit.localeCompare(cards[2].suit)==0 && cards[0].suit.localeCompare(cards[3].suit)==0 && cards[0].suit.localeCompare(cards[4].suit)==0) hands[4]++;
  //checks for flush

  if (hands[5]>0 && hands[4]>0) hands[1]++; //checks for straught flush

  if (hands[1]>0 && parseInt(cards[0].value)==10) hands[0]++; //checks for royal flush


  for (let i = 0; i < hands.length; i++)
  {
    if (hands[i]>0)
    {
      msg.innerText = "You got " + handMsgs[i] +"!";
      multiplier = handValues[i];
      hasHand = 1;
      break;
    }
  }
  if (hasHand==0) msg.innerText = "You lost :(";

  let txt = "";
  for (let i = 0; i < 9; i++)
  {
    txt += hands[i] + " ";
  }
  document.getElementById('hands').innerText = txt;
}
