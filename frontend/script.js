let mediaRecorder;
let audioChunks = [];

document.addEventListener('DOMContentLoaded', () => {
    const startBtn = document.getElementById('start-record');
    const stopBtn = document.getElementById('stop-record') || document.getElementById('stop-record-login');
    const recIndicator = document.getElementById('recIndicator');

    if (startBtn) {
        startBtn.addEventListener('click', async () => {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                mediaRecorder = new MediaRecorder(stream);
                audioChunks = [];

                mediaRecorder.ondataavailable = event => audioChunks.push(event.data);
                mediaRecorder.start();

                if (recIndicator) {
                    recIndicator.classList.remove('hidden');
                }

                startBtn.disabled = true;
                stopBtn.disabled = false;

            } catch (err) {
                alert("Microphone access denied.");
                console.error("Recording error:", err);
            }
        });
    }

    if (stopBtn) {
        stopBtn.addEventListener('click', async () => {
            if (!mediaRecorder || mediaRecorder.state === "inactive") return;

            mediaRecorder.stop();

            mediaRecorder.onstop = async () => {
                const blob = new Blob(audioChunks, { type: 'audio/wav' });
                const formData = new FormData();
                formData.append('audio', blob, 'voice.wav');

                const username = document.getElementById('username')?.value;
                const password = document.getElementById('password')?.value;

                formData.append('username', username);
                if (password) formData.append('password', password);

                const endpoint = stopBtn.id.includes('login') ? '/login' : '/register';
                try {
                    const res = await fetch(endpoint, {
                        method: 'POST',
                        body: formData
                    });

                    if (res.redirected) {
                        window.location.href = res.url;
                    } else {
                        alert(await res.text());
                    }
                } catch (error) {
                    console.error("Fetch failed:", error);
                    alert("Error occurred during voice upload.");
                }

                if (recIndicator) {
                    recIndicator.classList.add('hidden');
                }

                startBtn.disabled = false;
                stopBtn.disabled = true;
            };
        });
    }

    const registerBtn = document.getElementById('register-btn');
    if (registerBtn) {
        registerBtn.addEventListener('click', () => alert("Please upload voice to complete registration."));
    }

    const loginBtn = document.getElementById('login-btn');
    if (loginBtn) {
        loginBtn.addEventListener('click', () => alert("Please upload voice to login."));
    }
});
