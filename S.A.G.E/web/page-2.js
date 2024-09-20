document.addEventListener('DOMContentLoaded', () => {
    const techLines = document.querySelector('.tech-lines');

    // Create tech lines
    for (let i = 0; i < 50; i++) {
        const line = document.createElement('div');
        line.classList.add('line');
        line.style.width = `${Math.random() * 150 + 50}px`;
        line.style.height = `${Math.random() * 2 + 1}px`;
        line.style.top = `${Math.random() * 100}vh`;
        line.style.left = `${Math.random() * 100}vw`;
        line.style.animationDuration = `${Math.random() * 10 + 5}s`;
        line.style.animationDirection = Math.random() < 0.5 ? 'normal' : 'reverse';
        techLines.appendChild(line);
    }
    eel.start_assistant()();
});

async function logoutuser() {
    await eel.logoutuser()();
    window.location.href = 'page-1.html';
}