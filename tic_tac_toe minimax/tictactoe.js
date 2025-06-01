let board=[
    ['','',''],
    ['','',''],
    ['','','']
]

let ai='X';
let human='O';

let curr_player=human;

function setup(){
    createCanvas(400, 400);
    textSize(32);
    strokeWeight(4);
    w = width / 3;
    h = height / 3;

}


function draw() {
    background(255);

    line(w,0,w,height);
    line(w*2,0,w*2,height);
    line(0,h,width,h);
    line(0,h*2,width,h*2);


    for (let j = 0; j < 3; j++) {
      for (let i = 0; i < 3; i++) {
        let x = w * j + w/2;
        let y = h * i + h/2;
        let spot=board[i][j];
        if ( spot == human){
            noFill();
            ellipse(x,y,w/2);
        }
        else if(spot==ai){
            let xr=w/4;
            line(x-xr,y-xr,x+xr,y+xr);
            line(x+xr,y-xr,x-xr,y+xr);
        }
      }
    }


    let result = checkwinner();
    if (result != null) {
      noLoop();
      let resultP = createP('');
      resultP.style('font-size', '32pt');
      if (result == 'tie') {
        resultP.html('Tie!');
      } else {
        resultP.html(`${result} wins!`);
      }
    }

  }

function mousePressed(){
    if(curr_player==human){
        let i=floor(mouseX/w);
        let j=floor(mouseY/h);
        if(board[j][i]==''){
            board[j][i]=human;
            curr_player=ai;
            bestmove();
        }
    }
}

function checkwinner() {
    let winner = null;
  
    for (let i = 0; i < 3; i++) {
      if (board[i][0] != '' && board[i][0] == board[i][1] && board[i][1] == board[i][2]) {
        winner = board[i][0];
      }
      if (board[0][i] != '' && board[0][i] == board[1][i] && board[1][i] == board[2][i]) {
        winner = board[0][i];
      }
    }
  
    if (board[0][0] != '' && board[0][0] == board[1][1] && board[1][1] == board[2][2]) {
      winner = board[0][0];
    }
    if (board[0][2] != '' && board[0][2] == board[1][1] && board[1][1] == board[2][0]) {
      winner = board[0][2];
    }
  
    let openSpots = 0;
    for (let i = 0; i < 3; i++) {
      for (let j = 0; j < 3; j++) {
        if (board[i][j] == '') {
          openSpots++;
        }
      }
    }
  
    if(winner==null && openSpots==0){
      return 'tie';
    }else{
      return winner;
    }
  }
  

function bestmove(){
    let bestscore = -Infinity;
    let move;
    let available=[]
    for(let i=0;i<3;i++){
        for(let j=0;j<3;j++){
            if (board[i][j]==""){
               board[i][j]=ai;
              let score=minimax(board,0,false);
              board[i][j]='';
              if(score>bestscore){
                bestscore=score;
                move={i,j};
              }
            }
        }   
     }
    board[move.i][move.j]=ai
    curr_player=human;
}

let scores={
  X:10,
  O:-10,
  tie:0
};

function minimax(board,depth,maximizing){
    let result=checkwinner();
    if(result!=null){
      return scores[result];
    }

    if(maximizing){
      let bestscore=-Infinity;
      for(let i=0;i<3;i++){
        for(let j=0;j<3;j++){
          if (board[i][j]==""){
            board[i][j]=ai;
            let score=minimax(board,depth+1,false);
            board[i][j]='';
            bestscore=max(score,bestscore);
          }
        }
      }
      return bestscore;
    }else{
      let bestscore=Infinity;
      for(let i=0;i<3;i++){
        for(let j=0;j<3;j++){
          if(board[i][j]==""){
            board[i][j]=human;
            let score=minimax(board,depth+1,true);
            board[i][j]='';
            bestscore=min(score,bestscore);
          }
        }
      }
      return bestscore;
    }
}