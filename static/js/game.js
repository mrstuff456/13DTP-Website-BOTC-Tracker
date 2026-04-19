let seats = 5;
let selectedSeat = "";
let seatNotes = ["","","","",""];

document.addEventListener("DOMContentLoaded", innitializeGame())

function innitializeGame() {
    document.getElementById('seatMenu').hidden = true;
}

function createNewSeat() {
    if (seats < 20) {
        // identifiers
        const newSeat = document.createElement('div');
        const seatContainer = document.getElementsByClassName('main-circle-container');
        const root = document.querySelector(':root');

        const seatTokenImg = document.createElement('img');

        // add one to seats var and add a new item in the notes array
        seats += 1;
        root.style.setProperty('--seats', seats);
        seatNotes.push("");

        // add the required attributes to the new seat
        newSeat.classList.add('item');
        newSeat.style = `--i: ${seats}`;
        newSeat.id = `${seats}`;
        newSeat.setAttribute("onclick","seatMenu(this)")

        // add the required attributes to the token image
        seatTokenImg.classList.add('token-img');
        seatTokenImg.src = '/static/images/TokenBG.png';

        // append seat div and token image to the circle
        seatContainer[0].appendChild(newSeat);
        document.getElementById(seats).appendChild(seatTokenImg);

    }
}
    
function removeSeat() {
    if (seats > 5) {
        const root = document.querySelector(':root');

        document.getElementById(`${seats}`).remove();
        seats -= 1;
        seatNotes.splice(seats, 1);

        root.style.setProperty('--seats', seats);
    }
}

function seatMenu(seatId) {
    closeSeatMenu();

    seat = document.getElementById(seatId.id);
    selectedSeat = seat;
    console.log(selectedSeat)
    document.getElementById('seatNotes').value = seatNotes[seatId.id - 1];
    document.getElementById('seatMenu').hidden = false;
}

function closeSeatMenu() {
    seatNotes[selectedSeat.id - 1] = document.getElementById('seatNotes').value;
    document.getElementById('seatMenu').hidden = true;
}