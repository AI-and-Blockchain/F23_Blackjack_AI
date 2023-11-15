
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
var decklocation = [62.5/100, 31.2/100];
var userlocation = [47/100, 77/100];  
var cardoffset = [50, 10];
var card_backside = "./assets/Cards/backside.png";

var id = 0;
var bet_amount = 0;
var numDealerCards = 0;
var numPlayerCards = 0;
var cardList = [];
var hit_active = false;
var stand_active = false;
var bet_active = true;
var deal_active = false;
var player_name = 'angelica';
var playerObjects = []


//class
class Card{
  constructor(x, y, id, suit, value, angle) {
    this.x = x;
    this.y = y;
    this.id;
    this.sideup = -1; //1=front -1=back
    this.fliplocked = 0;
    this.suit =suit;
    this.value=value;
    this.angle = angle;
    this.card_count = 0;

  }
}

class Player{
  constructor(x, y,  name, address, angle, main_player) {
    this.x = x;
    this.y = y;
    this.name = name;
    this.address = address;
    this.angle = angle;
    this.main_player = main_player;
  }
}


//init game: call funcitons
init_game();


function init_game(){
  init_players();
  init_dealer_deck();
  new_game();
  document.addEventListener("click", flipcard);

}

function init_players(){
  main_player = new Player(userlocation[0], userlocation[1], player_name, 0, 0, 1);
  console.log(main_player.main_player);
  ai_player = new Player(userlocation[0]+0.17, userlocation[1]-0.06, "Mr.JokerPoker", 0, -5, 0);
  playerObjects.push(main_player, ai_player);
}

function deal(){
  if(deal_active){
    setTimeout(function(){deal_user_card()}, 20);
    setTimeout(function(){deal_user_card()}, 200);
    setTimeout(function(){deal_dealer_card()},700);
    setTimeout(function(){deal_dealer_card()}, 900);
    deal_active = false;
    bet_active = false;
    hit_active = true;
    stand_active = true;
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
    ctx.save();
    ctx.translate(card.x, card.y);
    ctx.rotate(Math.PI/card.angle);
    ctx.drawImage(cardimg, (cardoffset[0]*card.card_count), (cardoffset[1]*card.card_count), cardsize[0], cardsize[1]);
    ctx.restore();
  }

}

function init_dealer_deck(){
  ctx.beginPath();
  var x=decklocation[0]*width;
  var y=decklocation[1]*height;
  const card = new Card(x, y, 0, null, null);
  paintcard(card);
}


function deal_user_card(){
  for(let p of playerObjects){
    ctx.beginPath();
    var x=p.x*width;
    var y=p.y*height;
    var cardSuit = cardSuits[Math.ceil(Math.random()*100)%numSuits];
    var cardValue = cardValues[Math.ceil(Math.random()*100)%numValues];
    const card = new Card(x, y, id, cardSuit, cardValue, p.angle);
    card.card_count = p.card_count;
    id+=1;
    cardList.push(card);
    p.card_count +=1;
    console.log(p.main_player);
    if(p.main_player === 1){
      numPlayerCards+=1;
      card.fliplocked = 0;
      card.sideup = 1;
    }else{
      card.fliplocked = 1;
      card.sideup = -1;
    }
    paintcard(card);
  }
}

function deal_dealer_card(){
  ctx.beginPath();
  var x=decklocation[0]*width-(cardoffset[0]*numDealerCards)-200;
  var y=decklocation[1]*height- (cardoffset[1]*numDealerCards);
  var cardSuit = cardSuits[Math.ceil(Math.random()*100)%numSuits];
  var cardValue = cardValues[Math.ceil(Math.random()*100)%numValues];
  var card = new Card(x, y, id, cardSuit, cardValue);
  if(numDealerCards === 0){
    card.fliplocked = 1;
    card.sideup = -1; 
  }else{
    card.sideup = 1;
  }
  id+=1;
  numDealerCards+=1;
  cardList.push(card);
  paintcard(card);
}

function flipcard(event) {
  var mousex = event.clientX; 
  var mousey = event.clientY;
  for (let card of cardList) {
    x = card.x + cardoffset[0]*card.card_count;
    y = card.y + cardoffset[0]*card.card_count;
    if((x+cardsize[0] > mousex) && (x-cardsize[0] < mousex) && (y+cardsize[1] > mousey) && (y-cardsize[1] < mousey)){
      if(card.fliplocked === 0){
        card.sideup *= -1;
        paintcard(card);
      }else{
        paintcard(card);
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
      item.sideup = 1;
      item.fliplocked = 1;
      setTimeout(function(){paintcard(item)}, 200*j);
      j+=1
    }
    //reorder cards
    setTimeout(function(){
    for (let item of cardList) {
      paintcard(item);
    }}, 300*numPlayerCards);
 
    stand_active = false;
    hit_active = false;
    bet_active = true;
    bet_amount = 0;
  }
}

function new_game(){
  for(let p of playerObjects){
    p.card_count = 0;
  }
  numPlayerCards = 0;
  bet_amount = 0;
  numDealerCards = 0;
  cardList = [];
  hit_active = false;
  stand_active = false;
  bet_active = true;
  deal_active = false;
  repaint_canvas();
}

function repaint_canvas(){
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  init_dealer_deck();
  paint_playername();

}

function paint_playername(){
  for(let p of playerObjects){
    ctx.save();
    ctx.translate( (p.x+0.03) * width, (p.y+0.22) * height);
    ctx.rotate( Math.PI / p.angle );
    ctx.font = "bold 20px Arial";
    ctx.fillStyle = "black";
    ctx.textAlign = "center";
    ctx.fillText(`${p.name}`, p.angle*-20, p.angle*-2);
    ctx.restore();
  }
}

function bet_helper(a){
  if(bet_active){
    if(bet_amount===0){
      new_game();
    }
    repaint_canvas();
    deal_active = true;
    ctx.fillStyle = "gold";
    ctx.font = "20px Comic Sans";
    bet_amount = a;
    ctx.fillText(`+${bet_amount} WEI...`, 77/100*width, 37.5/100*height);
  }
}

function plus(){
  bet_helper(bet_amount + 10);
}
function minus(){
  if(bet_amount >10){
    bet_helper(bet_amount - 10);
  }
}


