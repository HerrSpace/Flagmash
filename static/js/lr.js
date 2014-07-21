document.onkeydown = checkKey;

function checkKey(e) {

    e = e || window.event;

    if (e.keyCode == '37') {
        document.getElementById('lefty').click();
    }
    else if (e.keyCode == '39') {
        document.getElementById('righty').click();
    }
}