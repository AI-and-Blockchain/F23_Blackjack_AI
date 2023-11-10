
//global vars
//colors
const backgroundcolor =  'rgb(217, 222, 200)';
const backgroundimage =  "./assets/blackjack_table.jpg";
const greycolor = "rgb(77, 79, 102)";
const redcolor = "rgb(178,51,81)";
const greencolor = "rgb(136,178,51)";
const lightgreen = "rgb(108, 120, 106)";
const yellowcolor = "rgb(217, 197, 141)"

//canvas
const canvas = document.querySelector('.myCanvas');
const width = canvas.width = window.innerWidth;
const height = canvas.height = window.innerHeight;
const ctx = canvas.getContext('2d');
ctx.background = backgroundimage;




//card vars
var cardsize = [80, 120];
var cardSuits = ["spades", "hearts", "clubs", "diamonds"];
var numSuits = 4;
var cardValues = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king", "ace"];
var numValues = 13;
console.log(width, height)
var decklocation = [10/16 * width, 230/735*height];
var userlocation = [71/160*width, 560/735*height];
var cardoffset = [50, 10];
var card_backside = "./assets/Cards/backside.png";

deal_active = false;
bet_active = true;
hit_active = false;
stand_active = false;


//class
class Card{
  constructor(x, y, id, suit, value) {
    this.x = x;
    this.y = y;
    this.id;
    this.sideup = -1; //1=front -1=back
    this.fliplocked = 0
    this.suit =suit;
    this.value=value;

  }
}

// function setButtoncolors(){
//   background-color: var(--btncolor);
// }

//call funcitons
init_dealer_deck();
new_game();
document.addEventListener("click", flipcard);


function deal(){
  if(deal_active){
    setTimeout(function(){deal_user_card()}, 20);
    setTimeout(function(){deal_user_card()}, 200);
    setTimeout(function(){deal_dealer_card()}, 200);
    deal_active = false;
  }
}



function paintcard(card){
  var cardimg = new Image(); 
  var cardSuit = card.suit
  var cardValue = card.value
  cardimg.src = `./assets/Cards/${cardValue}_of_${cardSuit}.png`;
  if(card.sideup ===-1){
    cardimg.src = card_backside;
  }
  cardimg.onload = function (e)
  {
      ctx.drawImage(cardimg, card.x, card.y, cardsize[0], cardsize[1]);
  }

}

function init_dealer_deck(){
  ctx.beginPath();
  var x=decklocation[0];
  var y=decklocation[1];
  const card = new Card(x, y, 0, null, null);
  paintcard(card);
}


function deal_user_card(){
  ctx.beginPath();
  var x=userlocation[0] + (cardoffset[0]*cardCount);
  var y=userlocation[1] + (cardoffset[1]*cardCount);
  var cardSuit = cardSuits[Math.ceil(Math.random()*100)%numSuits];
  var cardValue = cardValues[Math.ceil(Math.random()*100)%numValues];
  const card = new Card(x, y, id, cardSuit, cardValue);
  card.id = id;
  id+=1;
  cardList.push(card);
  console.log("user id", card.id)
  cardCount +=1;
  numPlayerCards+=1;
  paintcard(card);
  num_cards_dealt += 1;
}

function deal_dealer_card(){
  ctx.beginPath();
  var x=decklocation[0]-(cardoffset[0]*numDealerCards)-200;
  var y=decklocation[1]- (cardoffset[1]*numDealerCards);
  var cardSuit = cardSuits[Math.ceil(Math.random()*100)%numSuits];
  var cardValue = cardValues[Math.ceil(Math.random()*100)%numValues];
  var card = new Card(x, y, id, cardSuit, cardValue);
  if(numDealerCards === 0){
    card.fliplocked = 1;
    card.sideup = -1; 
  }else{
    card.sideup = 1;
  }
  card.id = id;
  id+=1;
  numDealerCards+=1;
  cardList.push(card);
  console.log("dealer id", card.id)
  cardCount;
  paintcard(card);
}

function flipcard(event) {
  var mousex = event.clientX; 
  var mousey = event.clientY;
  for (let item of cardList) {
    if((item.x+cardsize[0] > mousex) && (item.x-cardsize[0] < mousex) && (item.y+cardsize[1] > mousey) && (item.y-cardsize[1] < mousey)){
      if(item.fliplocked === 0){
        item.sideup *= -1;
        paintcard(item);
      }else{
        paintcard(item);
      }
      break;
    }
  } 
}

function hit() {
  if(hit_active){
    deal_user_card();
  }

}

function stand() {
  if(stand_active){
    
    for (let i = 0; i < numPlayerCards-2; i++) {
      setTimeout(function(){deal_dealer_card()}, 200*i);
    }
    var j=0;
    for (let item of cardList) {
      console.log(item.id);
      item.sideup = 1;
      item.fliplocked = 1;
      setTimeout(function(){paintcard(item)}, 200*j);
      j+=1
    }
    stand_active = false;
    hit_active = false;
    bet_active = true;
    bet_amount = 0;
  }
}

function new_game(){
  numPlayerCards = 0;
  bet_amount = 0;
  numDealerCards = 0;
  cardList = [];
  cardCount = 0;
  hit_active = false;
  stand_active = false;
  bet_active = true;
  deal_active = false;
  repaint_canvas();
}

function repaint_canvas(){
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  init_dealer_deck();
}

function bet (){
  if(bet_active){
    if(bet_amount===0){
      new_game();
    }
    repaint_canvas();
    deal_active = true;
    ctx.fillStyle = "gold";
    ctx.font = "20px Comic Sans";
    bet_amount += 10;
    ctx.fillText(`+${bet_amount} ETHER...`, 12/16*width, 270/735*height);
  }
}

