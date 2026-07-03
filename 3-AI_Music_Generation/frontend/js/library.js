const STORAGE_KEY = "musicgen_ai_library_v1";
const API_URL = "https://mussarat123shamsher-ai-music-generation.hf.space";

const libraryGrid = document.getElementById("libraryGrid");
const emptyState = document.getElementById("emptyState");
const searchInput = document.getElementById("searchInput");
const clearLibraryBtn = document.getElementById("clearLibraryBtn");

let currentAudio = null;

function getLibrary() {
  return JSON.parse(localStorage.getItem(STORAGE_KEY) || "[]");
}

function saveLibrary(items) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(items));
}

async function downloadUrl(url, filename) {

  try {

    const response = await fetch(url);

    if (!response.ok) {
      throw new Error("Download failed");
    }

    const blob = await response.blob();

    const blobUrl = URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = blobUrl;
    a.download = filename || "download";

    document.body.appendChild(a);
    a.click();
    a.remove();

    URL.revokeObjectURL(blobUrl);

  } catch (err) {

    console.error(err);
    alert("File not available at download time.");

  }
}

function downloadMidi(item) {

  if (!item || !item.midi_url) return;

  const midiUrl =
    item.midi_url.startsWith("http")
      ? item.midi_url
      : `${API_URL}${item.midi_url}`;

  downloadUrl(
    midiUrl,
    item.midi_filename || "generated.mid"
  );
}

function downloadAudio(item) {

  if (!item || !item.audio_url) return;

  const audioUrl =
    item.audio_url.startsWith("http")
      ? item.audio_url
      : `${API_URL}${item.audio_url}`;

  downloadUrl(
    audioUrl,
    item.audio_filename || "generated.wav"
  );
}

async function playAudio(item) {
  try {

    if (!item || !item.audio_url) {
      throw new Error("Missing audio_url.");
    }

    if (currentAudio) {
      try {
        currentAudio.pause();
      } catch {}
    }

    const audioUrl =
      item.audio_url.startsWith("http")
        ? item.audio_url
        : `${API_URL}${item.audio_url}`;

    currentAudio = new Audio(audioUrl);
    currentAudio.volume = 0.9;

    await currentAudio.play();

  } catch (err) {
    console.error(err);
  }
}

function deleteTrack(id) {
  const items = getLibrary();
  const updated = items.filter((item) => item.id !== id);
  saveLibrary(updated);
  renderLibrary();
}

function updateStats(items){

  document.getElementById("totalTracks")
    .textContent = items.length;

  document.getElementById("latestTrack")
    .textContent =
      items.length > 0
      ? "Active"
      : "None";

  const counter =
    document.getElementById("trackCounter");

  if(counter){
    counter.textContent =
      `${items.length} Track${items.length !== 1 ? "s" : ""}`;
  }
}

function renderLibrary(search = "") {
  const items = getLibrary();

  const filtered = items.filter((item) =>
    (item.seedNotes || "")
      .toLowerCase()
      .includes(String(search).toLowerCase())
  );

  updateStats(filtered);
  libraryGrid.innerHTML = "";

  if (!filtered.length) {
    emptyState.classList.remove("hidden");
    return;
  }

  emptyState.classList.add("hidden");

  filtered.forEach((item) => {
    const card = document.createElement("div");
    card.className = "track-card";

    card.innerHTML = `
      <h3 class="font-bold mb-3">${item.seedNotes || "Untitled"}</h3>
      <p class="text-white/60 text-sm mb-4">${new Date(item.createdAt).toLocaleString()}</p>

      <div class="flex flex-wrap gap-2">
        <button class="play-btn secondary-btn" data-id="${item.id}">▶ Play</button>
        <button class="download-audio-btn secondary-btn" data-id="${item.id}">⬇ Audio</button>
        <button class="download-midi-btn secondary-btn" data-id="${item.id}">⬇ MIDI</button>
        <button class="delete-btn secondary-btn" data-id="${item.id}">🗑 Delete</button>
      </div>
    `;

    libraryGrid.appendChild(card);
  });

  if (window.gsap) {
    gsap.from(".track-card", {
      y: 30,
      opacity: 0,
      stagger: 0.05,
      duration: 0.5,
    });
  }
}

searchInput.addEventListener("input", (e) => {
  renderLibrary(e.target.value);
});

clearLibraryBtn.addEventListener("click", () => {
  if (confirm("Clear all saved tracks?")) {
    localStorage.removeItem(STORAGE_KEY);
    renderLibrary();
  }
});

document.addEventListener("click", (e) => {
  const items = getLibrary();

  const play = e.target.closest(".play-btn");
  const dlAudio = e.target.closest(".download-audio-btn");
  const dlMidi = e.target.closest(".download-midi-btn");
  const del = e.target.closest(".delete-btn");


  if (play) {
    const item = items.find((x) => x.id === play.dataset.id);
    if (item) playAudio(item);
  }

  if (dlAudio) {
    const item = items.find((x) => x.id === dlAudio.dataset.id);
    if (item) downloadAudio(item);
  }

  if (dlMidi) {
    const item = items.find((x) => x.id === dlMidi.dataset.id);
    if (item) downloadMidi(item);
  }

  if (del) {
    deleteTrack(del.dataset.id);
  }
});

renderLibrary();

