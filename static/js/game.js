let seats = 5;
let selectedSeat = "";
let seatData = []

document.addEventListener("DOMContentLoaded", innitializeGame)

function innitializeGame() {
    document.getElementById('seatMenu').hidden = true;
    console.log("innit")

    seatData = JSON.parse(document.getElementById("seatData").dataset.seatData);
    gameData = JSON.parse(document.getElementById("gameData").dataset.gameData);
    console.log(seatData)
    // hide all menu elements
    document.getElementById('menu_seatNotes').hidden = true;
    document.getElementById('menu_seatName').hidden = true;
    document.getElementById('menu_seatClose').hidden = true;
    document.getElementById('menu_seatCharacter_BG').hidden = true;
    //document.getElementById('menu_seatTitle').hidden = true;

// make sure the number of displayed seats matches the amount of seats in the data
 while (seats < seatData.length) {
    createNewSeat(); 
 }
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
        if (seatData.length < seats) {
            seatData.push(["", 0, "", null, seats]);
        }

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
        seatData.splice(seats, 1);

        root.style.setProperty('--seats', seats);
    }
}

function seatMenu(seatId) {
    closeSeatMenu();

    seat = document.getElementById(seatId.id);
    selectedSeat = seat;
    console.log(selectedSeat)

    console.log("clicked id:", seatId.id);
    console.log("index:", seatId.id - 1);
    console.log("data:", seatData[seatId.id - 1]);

    document.getElementById('menu_seatNotes').value = seatData[seatId.id - 1][2];

    // show all the menu elements 
    document.getElementById('menu_seatNotes').hidden = false;
    document.getElementById('menu_seatName').hidden = false;
    document.getElementById('menu_seatClose').hidden = false;
    document.getElementById('menu_seatCharacter_BG').hidden = false;
    //document.getElementById('menu_seatTitle').hidden = false;
}

function closeSeatMenu() {
    // save the data of the notes tab
    if (selectedSeat) {
        seatData[selectedSeat.id - 1][2] =
            document.getElementById('menu_seatNotes').value;
    }

    // clear the notes tab's value
    //document.getElementById('menu_seatNotes').value = "";

    // hide all menu elements
    document.getElementById('menu_seatNotes').hidden = true;
    document.getElementById('menu_seatName').hidden = true;
    document.getElementById('menu_seatClose').hidden = true;
    document.getElementById('menu_seatCharacter_BG').hidden = true;
    //document.getElementById('menu_seatTitle').hidden = true;
}

function saveData() {
    closeSeatMenu();
    const fullGameData = [gameData, seatData];
    console.log(fullGameData)

    fetch('/save-game', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(fullGameData)
})
.then(response => response.json())
.then(data => {
    console.log('Success:', data);
})
.catch((error) => {
    console.error('Error:', error);
});
}