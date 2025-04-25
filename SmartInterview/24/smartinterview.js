let selectedField = null;
let selectedLevel = null;
let mediaRecorder;
let audioChunks = [];

function selectField(event) {
    selectedField = event.target.dataset.field;
    document.getElementById('selection-buttons').style.display = 'none';
    document.getElementById('level-buttons').style.display = 'flex';
}

function selectLevel(event) {
    selectedLevel = event.target.dataset.level;
    document.getElementById('level-buttons').style.display = 'none';
    startInterview();
}

async function startInterview() {
    const response = await fetch('/start_interview', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ field: selectedField, level: selectedLevel })
    });
    const data = await response.json();
    displayMessage(data.welcome_text, 'bot');
    playAudio(data.welcome_audio);
    document.getElementById('chat-input').style.display = 'flex';
}

function startRecording() {
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            mediaRecorder = new MediaRecorder(stream);
            mediaRecorder.start();
            
            mediaRecorder.addEventListener('dataavailable', event => {
                audioChunks.push(event.data);
            });

            mediaRecorder.addEventListener('stop', async () => {
                const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                const formData = new FormData();
                formData.append('audio', audioBlob);
                
                const response = await fetch('/process_audio', {
                    method: 'POST',
                    body: formData
                });
                const data = await response.json();
                displayMessage(data.transcript, 'user');
            });
            
            setTimeout(() => {
                mediaRecorder.stop();
            }, 5000); // 5 second recording limit
        });
}