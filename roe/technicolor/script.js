// Array of image paths (you need to have these images in the 'images' folder)
const images = [
    'images/processedegs13670_0.png',
    'images/processedegs13670_1.png',
    'images/processedegs13670_2.png',
    'images/processedegs13670_3.png',
    'images/processedegs13670_4.png',
    'images/processedegs13670_5.png',
    'images/processedegs13670_6.png',
    'images/processedegs13670_7.png',
    'images/processedegs13670_8.png',
    'images/processedegs13670_9.png'
  ];
  
  // Corresponding taglines for each image
  const taglines = [
    '115/150/200',
    '115/200/277',
    '115/277/356',
    '115/277/444',
    '150/200/356',
    '150/277/356',
    '150/277/444',
    '150/356/444',
    '200/277/356',
    '277/356/444'
   ];
  
// Function to get a random image and its tagline, and remove them from the pool
function getRandomImageAndTagline() {
    if (images.length === 0) {
      alert('No more images to display!');
      return null; // Return null if there are no more images
    }
    const randomIndex = Math.floor(Math.random() * images.length);
    const selectedImage = images[randomIndex];
    const selectedTagline = taglines[randomIndex];
  
    // Remove the selected image and tagline from the array
    images.splice(randomIndex, 1);
    taglines.splice(randomIndex, 1);
  
    return { image: selectedImage, tagline: selectedTagline };
  }
  
  // Function to set up event listeners for both images
  function setupImageClickHandlers() {
    const image1 = document.getElementById('image1');
    const tagline1 = document.getElementById('tagline1');
    const image2 = document.getElementById('image2');
    const tagline2 = document.getElementById('tagline2');
  
    image1.addEventListener('click', () => {
      const result = getRandomImageAndTagline();
      if (result) {
        image1.src = result.image;
        tagline1.textContent = result.tagline;
      }
    });
  
    image2.addEventListener('click', () => {
      const result = getRandomImageAndTagline();
      if (result) {
        image2.src = result.image;
        tagline2.textContent = result.tagline;
      }
    });
  }
  
  // Initialize event listeners when the page loads
  window.onload = setupImageClickHandlers;