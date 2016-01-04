$(document).foundation();

// Background Video
// Reference: https://codepen.io/dudleystorey/pen/knqyK
var vid = document.getElementById("bgvid");
var pauseButton = document.querySelector("#blowdry button");

function vidFade() {
    vid.classList.add("stopfade");
}

vid.addEventListener('ended', function()
{
    // only functional if "loop" is removed
    vid.pause();
    // to capture IE10
    vidFade();
});

pauseButton.addEventListener("click", function() {
    vid.classList.toggle("stopfade");
    if (vid.paused) {
    vid.play();
    pauseButton.innerHTML = "Pause";
    } else {
    vid.pause();
    pauseButton.innerHTML = "Paused";
    }
});