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
  

// Track the number of remaining images, the last image and tagline shown
let lastImageShown = null;
let lastTaglineShown = null;

// Function to get a random image and tagline, removing them from the pool
function getRandomImageAndTagline(excludeImage = null) {
  if (images.length === 0) {
    alert('No more images to display!');
    return null;
  }

  let availableImages = images;
  
  // Exclude the current image from the pool to avoid A and B being the same
  if (excludeImage !== null) {
    availableImages = images.filter(image => image !== excludeImage);
  }

  const randomIndex = Math.floor(Math.random() * availableImages.length);
  const selectedImage = availableImages[randomIndex];
  const selectedTagline = taglines[images.indexOf(selectedImage)];

  // Remove the selected image and tagline from the arrays
  const actualIndex = images.indexOf(selectedImage);
  images.splice(actualIndex, 1);
  taglines.splice(actualIndex, 1);

  return { image: selectedImage, tagline: selectedTagline };
}

// Function to set up event listeners for both images
function setupImageClickHandlers() {
  const image1 = document.getElementById('image1');
  const tagline1 = document.getElementById('tagline1');
  const image2 = document.getElementById('image2');
  const tagline2 = document.getElementById('tagline2');

  image1.addEventListener('click', () => {
    const result = getRandomImageAndTagline(image2.src);
    if (result) {
      image1.src = result.image;
      tagline1.textContent = result.tagline;
      lastImageShown = image1;
      lastTaglineShown = result.tagline; // Track the last tagline shown
    }
    checkForWinner();
  });

  image2.addEventListener('click', () => {
    const result = getRandomImageAndTagline(image1.src);
    if (result) {
      image2.src = result.image;
      tagline2.textContent = result.tagline;
      lastImageShown = image2;
      lastTaglineShown = result.tagline; // Track the last tagline shown
    }
    checkForWinner();
  });
}

// Function to check if we have a winner (i.e., no more images left)
function checkForWinner() {
  if (images.length === 0) {
    alert('The winner is: ' + lastTaglineShown);
    lastImageShown.style.border = '5px solid black'; // Add border to the winning image
  }
}

// Initialize event listeners when the page loads
window.onload = setupImageClickHandlers;