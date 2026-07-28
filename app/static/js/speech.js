let recorder;
let chunks = [];

const button = document.getElementById("recordButton");
const result = document.getElementById("speechResult");

button.onclick = async () => {

    const stream = await navigator.mediaDevices.getUserMedia({
        audio: true
    });

    recorder = new MediaRecorder(stream);

    recorder.start();

    button.innerText = "Grabando...";

    chunks = [];

    recorder.ondataavailable = e => {
        chunks.push(e.data);
    };

    setTimeout(() => recorder.stop(), 5000);

    recorder.onstop = async () => {

        button.innerText = "Procesando...";

        const blob = new Blob(chunks, {
            type: "audio/webm"
        });

        const form = new FormData();

        form.append("audio", blob, "audio.webm");

        const response = await fetch("/speech", {
            method: "POST",
            body: form
        });

        const data = await response.json();

        result.innerText = data.text;

        button.innerText = "🎤 Hablar";
    };
};