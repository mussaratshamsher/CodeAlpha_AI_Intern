// ===================================
// CONFIG
// ===================================

const API_URL = "https://mussarat123shamsher-ai-music-generation.hf.space";

const STORAGE_KEY = "musicgen_ai_library_v1";

// ===================================
// ELEMENTS
// ===================================

const genForm = document.getElementById("genForm");

const seedEl = document.getElementById("seedNotes");

const lengthEl = document.getElementById("length");

const tempEl = document.getElementById("temperature");

const tempValue =
document.getElementById("tempValue");

const generateBtn =
document.getElementById("generateBtn");

const playBtn =
document.getElementById("playBtn");

const downloadBtn =
document.getElementById("downloadBtn");

const statusEl =
document.getElementById("status");

const errorEl =
document.getElementById("error");

const recentTracks =
document.getElementById("recentTracks");

// ===================================
// STATE
// ===================================

let lastCreationId = null;

let audioCtx = null;

let activeNodes = [];

// ===================================
// HELPERS
// ===================================

function setStatus(text){
  statusEl.textContent = text;
}

function setError(text){
  errorEl.textContent = text || "";
}

function nowId(){
  return (
    "track_" +
    Date.now() +
    "_" +
    Math.random().toString(36).slice(2,8)
  );
}

function getLibrary(){
  return JSON.parse(
    localStorage.getItem(STORAGE_KEY) || "[]"
  );
}

function saveLibrary(items){
  localStorage.setItem(
    STORAGE_KEY,
    JSON.stringify(items)
  );
}

function bytesToBase64(bytes){

  let binary = "";

  bytes.forEach(
    b => binary += String.fromCharCode(b)
  );

  return btoa(binary);
}

function base64ToBytes(base64){

  const binary = atob(base64);

  const bytes =
  new Uint8Array(binary.length);

  for(let i=0;i<binary.length;i++){

    bytes[i] = binary.charCodeAt(i);

  }

  return bytes;
}

// ===================================
// TEMPERATURE
// ===================================

tempEl.addEventListener("input", () => {

  tempValue.textContent =
  Number(tempEl.value).toFixed(1);

});

// ===================================
// STATS
// ===================================

function updateStats(){

  document.getElementById("statNotes")
    .textContent = lengthEl.value;

  document.getElementById("statTemp")
    .textContent = Number(tempEl.value)
    .toFixed(1);

}

tempEl.addEventListener("input", updateStats);
lengthEl.addEventListener("input", updateStats);

updateStats();

// ===================================
// AUDIO PLAYBACK (HTML5)
// ===================================

let currentAudio = null;
let currentAudioSrc = null;

function stopPlayback(){
  if(currentAudio){
    try{
      currentAudio.pause();
    }catch(e){}
    currentAudio = null;
    currentAudioSrc = null;
  }
  activeNodes = [];
}

async function playAudio(item, {replay=false} = {}){
  try{

    if(!item || !item.audio_url){
      throw new Error("Missing audio_url in history item.");
    }

    const audioUrl =
      item.audio_url.startsWith("http")
        ? item.audio_url
        : `${API_URL}${item.audio_url}`;

    // Toggle pause if same track is already playing
    if(
      currentAudio &&
      currentAudioSrc === audioUrl &&
      !currentAudio.paused
    ){
      currentAudio.pause();
      return "paused";
    }

    // Resume if same track is paused
    if(
      currentAudio &&
      currentAudioSrc === audioUrl &&
      currentAudio.paused
    ){
      await currentAudio.play();
      return "playing";
    }

    stopPlayback();

    console.log("Playing:", audioUrl);

    const audio = new Audio(audioUrl);
    audio.preload = "auto";
    audio.volume = 0.9;

    currentAudio = audio;
    currentAudioSrc = audioUrl;

    audio.addEventListener("ended", () => {
      currentAudio = null;
      currentAudioSrc = null;

      document
        .querySelectorAll(".play-track")
        .forEach(btn => {
          btn.innerHTML = "▶ Play";
        });
    });

    await audio.play();

    return "playing";

  }catch(err){
    console.error(err);
    setError(
      "Audio playback failed. " +
      (err?.message || "")
    );
  }
}


// ===================================
// DOWNLOAD
// ===================================

async function downloadUrl(url, filename){

  try{

    const response = await fetch(url);

    if(!response.ok){
      throw new Error("Download failed");
    }

    const blob = await response.blob();

    const blobUrl =
      window.URL.createObjectURL(blob);

    const a =
      document.createElement("a");

    a.href = blobUrl;
    a.download =
      filename || "download";

    document.body.appendChild(a);
    a.click();
    a.remove();

    window.URL.revokeObjectURL(blobUrl);

  }catch(err){

    console.error(err);

    setError(
      "Failed to download file."
    );

  }

}

function downloadMidi(item){

  if(item && item.midi_url){

    const midiUrl =
      item.midi_url.startsWith("http")
        ? item.midi_url
        : `${API_URL}${item.midi_url}`;
console.log("MIDI URL:", midiUrl);
    downloadUrl(
      midiUrl,
      item.midi_filename || "generated.mid"
    );

    return;
  }

  if(item && item.base64){

    const bytes = base64ToBytes(item.base64);

    const blob = new Blob(
      [bytes],
      {type:"audio/midi"}
    );

    const url =
      URL.createObjectURL(blob);

    const a =
      document.createElement("a");

    a.href = url;
    a.download =
      item.filename || "generated.mid";

    document.body.appendChild(a);
    a.click();
    a.remove();

    URL.revokeObjectURL(url);
  }
}

function downloadAudio(item){

  if(item && item.audio_url){

    const audioUrl =
      item.audio_url.startsWith("http")
        ? item.audio_url
        : `${API_URL}${item.audio_url}`;
console.log("Audio URL:", audioUrl);
    downloadUrl(
      audioUrl,
      item.audio_filename || "generated.wav"
    );

    return;
  }

  setError(
    "Audio not available for download."
  );
  
}


// ===================================
// RENDER RECENT
// ===================================

function renderRecent(){

  const items = getLibrary();

  recentTracks.innerHTML = "";

  items.slice(0,4).forEach(item => {

    const card =
    document.createElement("div");

    card.className =
    "track-card";

    card.innerHTML = `

      <h3 class="font-bold mb-2">
        ${item.seedNotes || "Untitled"}
      </h3>

      <p class="text-white/60 text-sm mb-4">
        ${new Date(
          item.createdAt
        ).toLocaleString()}
      </p>

      <div class="flex gap-2">

        <button
          class="play-track secondary-btn"
          data-id="${item.id}"
        >
          ▶ Play
        </button>

        <button
          class="pause-track secondary-btn"
          data-id="${item.id}"
          style="display:none"
        >
          ⏸ Pause
        </button>

        <button
          class="replay-track secondary-btn"
          data-id="${item.id}"
          style="display:none"
        >
          ↻ Replay
        </button>

        <button
          class="download-audio secondary-btn"
          data-id="${item.id}"
        >
          ⬇ Audio
        </button>

        <button
          class="download-midi secondary-btn"
          data-id="${item.id}"
        >
          ⬇ MIDI
        </button>


      </div>
    `;

    recentTracks.appendChild(card);

  });

}

renderRecent();

// ===================================
// RECENT EVENTS
// ===================================

document.addEventListener("click",(e)=>{

  const play = e.target.closest(".play-track");
  const pause = e.target.closest(".pause-track");
  const replay = e.target.closest(".replay-track");
  const downloadAudioBtn = e.target.closest(".download-audio");
  const downloadMidiBtn = e.target.closest(".download-midi");

  const items = getLibrary();

  if(play){

  const item = items.find(
    x => x.id === play.dataset.id
  );

  if(item){

    playAudio(item).then(state => {

      if(state === "paused"){
        play.innerHTML = "▶ Play";
      }

      if(state === "playing"){
        play.innerHTML = "⏸ Pause";
      }

    });

  }
}

  if(pause){
    if(currentAudio){
      try{ currentAudio.pause(); }catch(err){}
    }
  }

  if(replay){
    const item = items.find(x => x.id === replay.dataset.id);
    if(item){
      playAudio(item, {replay:true});
    }
  }

  if(downloadAudioBtn){
    const item = items.find(x => x.id === downloadAudioBtn.dataset.id);
    if(item){
      downloadAudio(item);
    }
  }

  if(downloadMidiBtn){
    const item = items.find(x => x.id === downloadMidiBtn.dataset.id);
    if(item){
      downloadMidi(item);
    }
  }

});


// ===================================
// GENERATE
// ===================================

genForm.addEventListener(
"submit",
async (e)=>{

e.preventDefault();

setError("");

const payload = {

  seed_notes:
  seedEl.value.trim(),

  length:
  Number(lengthEl.value),

  temperature:
  Number(tempEl.value),

  filename:
  "generated.mid"

};

generateBtn.disabled = true;

setStatus(
  "🎼 Generating music..."
);

try{

const response =
await fetch(
`${API_URL}/generate`,
{
method:"POST",

headers:{
"Content-Type":
"application/json"
},

body:
JSON.stringify(payload)

}
);

if(!response.ok){

throw new Error(
"Generation failed"
);

}

const data = await response.json();

const track = {

  id: nowId(),
  createdAt: Date.now(),
  seedNotes: data.seed_notes || payload.seed_notes,
  length: data.length || payload.length,
  temperature: data.temperature || payload.temperature,
  midi_filename: data.midi_filename,
  midi_url: data.midi_url,
  audio_filename: data.audio_filename,
  audio_url: data.audio_url

};


const items =
getLibrary();

items.unshift(track);

saveLibrary(
items.slice(0,30)
);

lastCreationId =
track.id;

downloadBtn.disabled =
false;

playBtn.disabled =
false;

renderRecent();

setStatus("✅ Music generated successfully. Playing...");
playAudio(track);


}catch(err){

console.error(err);

setError(
err.message
);

setStatus("Ready");

}

generateBtn.disabled = false;

});

// ===================================
// MAIN BUTTONS
// ===================================

playBtn.addEventListener(
"click",
()=>{

const items =
getLibrary();

const item =
items.find(
x=>x.id===lastCreationId
);

  if(item){

playAudio(item);

}

});

downloadBtn.addEventListener(
"click",
()=>{

const items =
getLibrary();

const item =
items.find(
x=>x.id===lastCreationId
);

  if(item){

downloadAudio(item);

}

});
