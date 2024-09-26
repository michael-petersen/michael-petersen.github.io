// Image Quiz Logic
const imageChoices = document.querySelectorAll('.image-choice');
const resultText = document.getElementById('quiz-result');

imageChoices.forEach(choice => {
    choice.addEventListener('click', () => {
        const isCorrect = choice.getAttribute('data-correct') === 'true';
        resultText.classList.remove('hidden');
        if (isCorrect) {
            resultText.textContent = "Correct!";
            resultText.classList.add('correct');
            resultText.classList.remove('incorrect');
        } else {
            resultText.textContent = "Try again!";
            resultText.classList.add('incorrect');
            resultText.classList.remove('correct');
        }
    });
});
