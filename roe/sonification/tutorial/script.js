// Image Quiz Logic
const imageChoices = document.querySelectorAll('.image-choice');
const resultText = document.getElementById('quiz-result');

imageChoices.forEach(choice => {
    choice.addEventListener('click', () => {
        const isCorrect = choice.getAttribute('data-correct') === 'true';
        resultText.classList.remove('hidden');
        if (isCorrect) {
            resultText.textContent = "This galaxy is Galaxy A!";
            resultText.classList.add('correct');
            resultText.classList.remove('incorrect');
        } else {
            resultText.textContent = "This galaxy is Galaxy B!";
            resultText.classList.add('incorrect');
            resultText.classList.remove('correct');
        }
    });
});

// Scroll to top and reset the quiz output when the button is clicked
document.getElementById('back-to-top').addEventListener('click', () => {
    // Reset the quiz result text and classes
    const resultText = document.getElementById('quiz-result');
    resultText.classList.add('hidden');  // Hide the result text
    resultText.textContent = '';         // Clear the text
    resultText.classList.remove('correct', 'incorrect'); // Remove any previous result classes

    // Reset all videos and audio elements to the beginning
    const videos = document.querySelectorAll('video');
    const audios = document.querySelectorAll('audio');
    
    videos.forEach(video => {
        video.pause();              // Pause the video
        video.currentTime = 0;      // Reset video to the beginning
    });
    
    audios.forEach(audio => {
        audio.pause();              // Pause the audio
        audio.currentTime = 0;      // Reset audio to the beginning
    });
    
    // Smooth scroll to the top
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
    
});