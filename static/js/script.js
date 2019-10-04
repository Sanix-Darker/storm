
const player = document.querySelector('.player');
const video = player.querySelector('.player-video');
const progress = player.querySelector('.progress');
const progressFilled = player.querySelector('.filled-progress');
const toggle = player.querySelector('.toggle-play');
const skippers = player.querySelectorAll('[data-skip]');
const ranges = player.querySelectorAll('.player-slider');
const fullscreen = player.querySelectorAll('#fullscreen')[0];

// Logic
// Play and pause of the video
const togglePlay = () => {
  if( window.innerHeight !== screen.height) {
    const playState = video.paused ? 'play' : 'pause';
    video[playState](); // Call play or paused method
  }
}

// To toggle the fullscreen
const toggleFullscreen = () => {
  const p = video;
  if( window.innerHeight !== screen.height) {
    // browser is not fullscreen
    let fn_enter = video.requestFullscreen || video.webkitRequestFullscreen || video.mozRequestFullScreen || video.oRequestFullscreen || video.msRequestFullscreen;
    fn_enter.call(video);
  } else {
      let fn_exit = video.exitFullScreen || video.webkitExitFullScreen || video.mozExitFullScreen || video.oExitFullScreen || video.msExitFullScreen;
      fn_exit.call(video);
  }
}

const updateButton = () => {
  const togglePlayBtn = document.querySelector('.toggle-play');
  if (this.paused) {
    togglePlayBtn.innerHTML = `<svg class="" width="16" height="16" viewBox="0 0 16 16"><title>play</title><path d="M3 2l10 6-10 6z"></path></svg>`;
  } else {
    togglePlayBtn.innerHTML = `<svg width="16" height="16" viewBox="0 0 16 16"><title>pause</title><path d="M2 2h5v12H2zm7 0h5v12H9z"></path></svg>`;
  }
}

const skip = () => {
  video.currentTime += parseFloat(this.dataset.skip);
}

const rangeUpdate = () => {
  video[this.name] = this.value;
}

const progressUpdate = () =>  {
  const percent = video.currentTime / video.duration * 100;
  progressFilled.style.flexBasis = `${percent}%`;
}

const scrub = (e) => {
  const scrubTime = e.offsetX / progress.offsetWidth * video.duration;
  video.currentTime = scrubTime;
}

// Event listeners
video.addEventListener('click', togglePlay);
video.addEventListener('play', updateButton);
video.addEventListener('pause', updateButton);
video.addEventListener('timeupdate', progressUpdate);
toggle.addEventListener('click', togglePlay);
fullscreen.addEventListener('click', toggleFullscreen);


skippers.forEach(button => button.addEventListener('click', skip));
ranges.forEach(range => range.addEventListener('change', rangeUpdate));
ranges.forEach(range => range.addEventListener('mousemove', rangeUpdate));

let mousedown = false;
progress.addEventListener('click', scrub);
progress.addEventListener('mousemove', e => mousedown && scrub(e));
progress.addEventListener('mousedown', () => mousedown = true);
progress.addEventListener('mouseup', () => mousedown = false);



let xhttp;
if (window.XMLHttpRequest) {
  // code for modern browsers
  xhttp = new XMLHttpRequest();
} else {
  // code for IE6, IE5
  xhttp = new ActiveXObject("Microsoft.XMLHTTP");
}
const loadContainer = () => {

  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      const videos = JSON.parse(this.responseText)["videos"]
      let video_list = "<ul id='myUL'>";
      for (var i = 0; i < (videos.length); i++){
          const link = videos[i];
          const link_splitted = link.split("/");
          const title = link_splitted[link_splitted.length - 1];
          video_list += "<li onclick='start_video(\""+title+"\", \""+link+"\")' class='video_id' id='"+link+"' title='"+title+"'>"+title.substring(0, 35);+"</li>";
      }
      video_list += "</ul>";
      document.getElementById("container").innerHTML = video_list;
    }
  };
  xhttp.open("GET", "/getall", true);
  xhttp.send();
}

const start_video = (title, link) => {
  document.getElementById("videoPlayer").src = link;
  document.getElementById("thetitle").innerHTML = title.substring(0, 80);
  console.log("Starting... "+title);
  togglePlay()
}

const Filter = () => {
  // Declare variables
  var input, filter, ul, li, a, i, txtValue;
  input = document.getElementById('search_box');
  filter = input.value.toUpperCase();
  ul = document.getElementById("myUL");
  li = ul.getElementsByTagName('li');

  // Loop through all list items, and hide those who don't match the search query
  for (i = 0; i < li.length; i++) {
    txtValue = li[i].textContent || li[i].innerText;
    if (txtValue.toUpperCase().indexOf(filter) > -1) {
      li[i].style.display = "";
    } else {
      li[i].style.display = "none";
    }
  }
}

const scrollToBottom = (id) => {
  var myDiv = document.getElementById(id);
  window.scrollTo(0, myDiv.innerHeight);
  setTimeout(() => {
    var myDiv = document.getElementById(id);
    window.scrollTo(0, myDiv.innerHeight);
  }, 100)
}