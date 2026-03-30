let seats = 5;
function createNewSeat() {
    if (seats < 20) {
        const newSeat = document.createElement('div');
        const seatContainer = document.getElementsByClassName('main-circle-container');
        const root = document.querySelector(':root');

        const seatTokenImg = document.createElement('img');

        seats += 1;

        newSeat.classList.add('item');
        newSeat.style = `--i: ${seats}`;
        newSeat.id = `${seats}`;

        seatTokenImg.classList.add('token-img');
        seatTokenImg.src = '/static/images/TokenBG.png';

        seatContainer[0].appendChild(newSeat);
        document.getElementById(seats).appendChild(seatTokenImg);
    
        root.style.setProperty('--seats', seats);
    }
}
    
function removeSeat() {
    if (seats > 5) {
        const root = document.querySelector(':root');

        document.getElementById(`${seats}`).remove();
        seats -= 1;

        root.style.setProperty('--seats', seats);
    }
}

