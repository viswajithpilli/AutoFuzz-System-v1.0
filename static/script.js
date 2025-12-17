document.getElementById('fuzzBtn').addEventListener('click', async () => {
    const binaryPath = document.getElementById('binaryPath').value;
    const fuzzBtn = document.getElementById('fuzzBtn');
    const consoleDiv = document.getElementById('consoleOutput');
    const statusVal = document.getElementById('statusValue');
    const offsetVal = document.getElementById('offsetValue');

    if (!binaryPath) return;

    // UI State: Running
    fuzzBtn.disabled = true;
    fuzzBtn.innerText = "EXECUTING...";
    consoleDiv.innerHTML = '<div class="info">[*] Initializing Fuzz Sequence...</div>';
    statusVal.className = "stat-value safe";
    statusVal.innerText = "SCANNING";
    offsetVal.innerText = "---";

    try {
        consoleDiv.innerHTML += `<div class="log">[*] Target: ${binaryPath}</div>`;
        consoleDiv.innerHTML += `<div class="log">[*] Injecting Payload...</div>`;

        const response = await fetch('/api/fuzz', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ binary_path: binaryPath })
        });

        const result = await response.json();

        // Check response
        if (response.status !== 200) {
            consoleDiv.innerHTML += `<div class="error">[-] Error: ${result.error}</div>`;
            statusVal.innerText = "ERROR";
            return;
        }

        // Process Result
        consoleDiv.innerHTML += `<div class="log">[*] Return Code: ${result.return_code}</div>`;

        if (result.crashed) {
            consoleDiv.innerHTML += `<div class="error">[+] CRASH CONFIRMED!</div>`;
            statusVal.innerText = "VULNERABLE";
            statusVal.className = "stat-value vulnerable";

            if (result.eip) {
                consoleDiv.innerHTML += `<div class="success">[+] EIP Control: ${result.eip}</div>`;
                if (result.offset) {
                    consoleDiv.innerHTML += `<div class="success">[+] EXACT OFFSET: ${result.offset}</div>`;
                    offsetVal.innerText = result.offset + " BYTES";
                } else {
                    consoleDiv.innerHTML += `<div class="log">[-] Offset calculation failed</div>`;
                    offsetVal.innerText = "UNKNOWN";
                }
            } else {
                consoleDiv.innerHTML += `<div class="log">[-] Could not extract EIP (GDB missing?)</div>`;
                offsetVal.innerText = "N/A";
            }
        } else {
            consoleDiv.innerHTML += `<div class="info">[-] Target did not crash. Secure.</div>`;
            statusVal.innerText = "SECURE";
            statusVal.className = "stat-value safe";
        }

    } catch (e) {
        consoleDiv.innerHTML += `<div class="error">[-] System Exception: ${e}</div>`;
    } finally {
        fuzzBtn.disabled = false;
        fuzzBtn.innerText = "INITIATE_FUZZ";
    }
});
