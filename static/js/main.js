/* === KITCHEN GAME === */
function startKitchenGame() {
    const field = document.getElementById('gameField');
    const caughtEl = document.getElementById('caught');
    const missedEl = document.getElementById('missed');
    const result = document.getElementById('kitchenResult');
    let caught = 0, missed = 0;

    const TARGET = 3;  // было 5
    const MAX_MISS = 3;

    const spawnInterval = setInterval(() => {
        if (caught >= TARGET || missed >= MAX_MISS) {
            clearInterval(spawnInterval);
            return;
        }
        const p = document.createElement('div');
        p.className = 'falling-pumpkin';
        p.textContent = '🎃';
        p.style.left = Math.random() * 85 + '%';
        p.style.top = '-50px';
        field.appendChild(p);

        let y = -50;
        const fall = setInterval(() => {
            y += 2;  // было 3 — теперь медленнее
            p.style.top = y + 'px';
            if (y > 400) {
                clearInterval(fall);
                p.remove();
                missed++;
                missedEl.textContent = missed + ' / ' + MAX_MISS;
                if (missed >= MAX_MISS) endGame(false);
            }
        }, 40);  // было 30 — теперь медленнее

        p.onclick = () => {
            clearInterval(fall);
            p.remove();
            caught++;
            caughtEl.textContent = caught + ' / ' + TARGET;
            if (caught >= TARGET) endGame(true);
        };
    }, 1200);  // было 800 — теперь реже появляются

    function endGame(win) {
        clearInterval(spawnInterval);
        if (win) {
            result.classList.remove('hidden');
            result.innerHTML = `<div class="success-box">
                <p>✅ You caught all pumpkins!</p>
                <p>You found: <b>🎃 ${KITCHEN_INGREDIENT}</b></p>
            </div>`;
            fetch(KITCHEN_WIN_URL, { method: 'POST' });
        } else {
            result.classList.remove('hidden');
            result.innerHTML = `<div class="warning-box">
                <p>💀 Too many pumpkins escaped!</p>
                <a href="/kitchen" class="btn">🔄 Try Again</a>
            </div>`;
        }
    }
}

/* === GARDEN GAME === */
function startGardenGame() {
    const bushes = document.querySelectorAll('.bush');
    const result = document.getElementById('gardenResult');
    let attempts = 0;

    bushes.forEach(bush => {
        bush.onclick = () => {
            attempts++;
            if (bush.dataset.flower === 'true') {
                bush.textContent = '🌸';
                bush.classList.add('found');
                result.classList.remove('hidden');
                result.innerHTML = `<div class="success-box">
                    <p>✅ You found the Moonflower in ${attempts} attempts!</p>
                    <p>You found: <b>🌸 ${GARDEN_INGREDIENT}</b></p>
                    <a href="/hall" class="btn">← Back to Hall</a>
                </div>`;
                fetch(GARDEN_WIN_URL, { method: 'POST' });
            } else {
                bush.textContent = '💨';
                setTimeout(() => { bush.textContent = ''; }, 500);
            }
        };
    });
}

/* === ATTIC MEMORY GAME === */
function startMemoryGame() {
    const display = document.getElementById('memoryDisplay');
    const buttons = document.querySelectorAll('.mem-btn');
    const status = document.getElementById('memoryStatus');

    let sequence = [];
    let playerSequence = [];
    let round = 0;
    const maxRounds = 3;

    function showSequence() {
        status.textContent = 'Watch carefully...';
        buttons.forEach(b => b.disabled = true);

        sequence = [];
        for (let i = 0; i < round + 2; i++) {
            sequence.push(ATTIC_SYMBOLS[Math.floor(Math.random() * ATTIC_SYMBOLS.length)]);
        }

        let i = 0;
        const showInterval = setInterval(() => {
            display.textContent = sequence[i];
            i++;
            if (i >= sequence.length) {
                clearInterval(showInterval);
                setTimeout(() => {
                    display.textContent = '';
                    status.textContent = 'Your turn! Repeat the sequence.';
                    buttons.forEach(b => b.disabled = false);
                    playerSequence = [];
                }, 1000);
            }
        }, 1000);
    }

    buttons.forEach(btn => {
        btn.onclick = () => {
            const symbol = btn.dataset.symbol;
            playerSequence.push(symbol);
            display.textContent = symbol;

            const idx = playerSequence.length - 1;
            if (playerSequence[idx] !== sequence[idx]) {
                status.textContent = '❌ Wrong! Try again...';
                setTimeout(() => {
                    playerSequence = [];
                    showSequence();
                }, 1500);
                return;
            }

            if (playerSequence.length === sequence.length) {
                round++;
                if (round >= maxRounds) {
                    status.textContent = '✅ You won!';
                    fetch(ATTIC_WIN_URL, { method: 'POST' });
                    setTimeout(() => { location.reload(); }, 2000);
                } else {
                    status.textContent = `✅ Round ${round}/${maxRounds} complete!`;
                    setTimeout(showSequence, 1500);
                }
            }
        };
    });

    setTimeout(showSequence, 1000);
}

/* === CAULDRON — drag ingredients to order === */
document.addEventListener('DOMContentLoaded', () => {
    const pool = document.getElementById('ingPool');
    const list = document.getElementById('orderList');
    if (!pool || !list) return;

    const order = [];

    pool.addEventListener('click', e => {
        const chip = e.target.closest('.ing-chip');
        if (!chip || chip.classList.contains('used')) return;

        order.push(chip.dataset.name);
        chip.classList.add('used');

        const li = document.createElement('li');
        li.textContent = chip.dataset.name;
        li.onclick = () => {
            const idx = order.indexOf(chip.dataset.name);
            order.splice(idx, 1);
            li.remove();
            chip.classList.remove('used');
            updateInput();
        };
        list.appendChild(li);
        updateInput();
    });

    function updateInput() {
        const form = document.getElementById('potionForm');
        if (!form) return;
        form.querySelectorAll('input[name="order"]').forEach(i => i.remove());
        order.forEach(name => {
            const inp = document.createElement('input');
            inp.type = 'hidden';
            inp.name = 'order';
            inp.value = name;
            form.appendChild(inp);
        });
    }
});