// Image Quiz Logic
const imageChoices = document.querySelectorAll('.image-choice');
const resultText = document.getElementById('quiz-result');

imageChoices.forEach(choice => {
    choice.addEventListener('click', () => {
        const isCorrect = choice.getAttribute('data-correct') === 'true';
        resultText.classList.remove('hidden');
        if (isCorrect) {
            resultText.textContent = "This galaxy generated the sound above!";
            resultText.classList.add('correct');
            resultText.classList.remove('incorrect');
        } else {
            resultText.textContent = "This galaxy generated the sound below!";
            resultText.classList.add('incorrect');
            resultText.classList.remove('correct');
        }
    });
});

// Scroll to top when the button is clicked
document.getElementById('back-to-top').addEventListener('click', () => {
    window.scrollTo({
        top: 0,
        behavior: 'smooth' // Smooth scroll back to the top
    });
});