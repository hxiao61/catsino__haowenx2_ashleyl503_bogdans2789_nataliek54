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
    if (cards[i].value.localeCompare("JACK")) cards[i].value = "11";
    else if (cards[i].value.localeCompare("QUEEN")) cards[i].value = "12";
    else if (cards[i].value.localeCompare("KING")) cards[i].value = "13";
    else if (cards[i].value.localeCompare("ACE")) cards[i].value = "14";
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
  0 = royal flush
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

  for (let i = 1; i < cards.length; i++)
  //checking for ONE PAIRs, THREE OF A KIND and FOUR OF A KIND
  {
    if (parseInt(hands.cards[i].value) == parseInt(hands.cards[i-1].value))
    {
      if (i<cards.length-1 && (parseInt(hands.cards[i].value) == parseInt(hands.cards[i+1].value)))
      {
        hands[7]++;
        i+=2;
      }
      if (i<cards.length-2 && (parseInt(hands.cards[i].value) == parseInt(hands.cards[i+2].value)))
      {
        hands[2]++;
        i+=3;
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

  if (parseInt(hands.cards[4].value)==parseInt(hands.cards[3].value)+1 && parseInt(hands.cards[3].value)==parseInt(hands.cards[2].value)+1 && parseInt(hands.cards[2].value)==parseInt(hands.cards[1].value)+1 && parseInt(hands.cards[1].value)==parseInt(hands.cards[0].value)+1) hands[5]++;
  else if (parseInt(hands.cards[4].value)==13 && parseInt(hands.cards[0].value)==2 && parseInt(hands.cards[3].value)==parseInt(hands.cards[2].value)+1 && parseInt(hands.cards[2].value)==parseInt(hands.cards[1].value)+1 && parseInt(hands.cards[1].value)==parseInt(hands.cards[0].value)+1) hands[5]++;
  //checks for straight

  if (!cards[0].suit.localeCompare(cards[1].suit) && !cards[0].suit.localeCompare(cards[2].suit) && !cards[0].suit.localeCompare(cards[3].suit) && !cards[0].suit.localeCompare(cards[4].suit)) hands[4]++;
  //checks for flush

  if (hands[5] && hands[4]) hands[1]++; //checks for straught flush

  if (hands[1] && parseInt(hands.cards[0].value)==10) hands[0]++; //checks for royal flush


  for (let i = 0; i < hands.length; i++)
  {
    if (hands[i])
    {
      msg.innerText = "You got " + handMsgs[i] +"!";
      multiplier = handValues[i];
      hasHand = 1;
      break;
    }
  }
  if (hasHand==0) msg.innerText = "You lost :(";
}
