// Information to display
let displayImage;
let displayHeadline = "";
let displayLocation = "";
let displayFont = ""
let displaySize;
let headline_padding;
let currentCharacter = 0;
let headlineType = "";
let letterFill;
let strokeFill;
let strokeThickness;

// Data tables
let good_place_bad_headline_table;
let bad_place_good_headline_table;

// Array of font names
let fonts = ['Anton', 'Bebas Neue', 'Crimson Text', 'DM Serif Display', 'Fjalla One', 'Noto Serif', 'Oswald', 'Playfair Display'];

// Mood of last headline shown
let lastHeadlineMood = 'bad';


function getStateFullName(stateCode) {
  // Mapping of state abbreviations to full names
  const stateMap = {
    "AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas", "CA": "California",
    "CO": "Colorado", "CT": "Connecticut", "DE": "Delaware", "FL": "Florida", "GA": "Georgia",
    "HI": "Hawaii", "ID": "Idaho", "IL": "Illinois", "IN": "Indiana", "IA": "Iowa",
    "KS": "Kansas", "KY": "Kentucky", "LA": "Louisiana", "ME": "Maine", "MD": "Maryland",
    "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota", "MS": "Mississippi", "MO": "Missouri",
    "MT": "Montana", "NE": "Nebraska", "NV": "Nevada", "NH": "New Hampshire", "NJ": "New Jersey",
    "NM": "New Mexico", "NY": "New York", "NC": "North Carolina", "ND": "North Dakota", "OH": "Ohio",
    "OK": "Oklahoma", "OR": "Oregon", "PA": "Pennsylvania", "RI": "Rhode Island", "SC": "South Carolina",
    "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas", "UT": "Utah", "VT": "Vermont",
    "VA": "Virginia", "WA": "Washington", "WV": "West Virginia", "WI": "Wisconsin", "WY": "Wyoming",
  };

  // Return the full state name corresponding to the state code
  return stateMap[stateCode] || stateCode; 
}

function preload() {
  good_place_bad_headline_table= loadTable('/data/SAIPE_Data - Good Place, Bad Headline.tsv', 'tsv', 'header');
  bad_place_good_headline_table= loadTable('/data/SAIPE_Data - Bad Place, Good Headline.tsv', 'tsv', 'header');
}

function setup() {
  // Full browser canvas
  resizeCanvas(windowWidth, windowHeight);
  // Presentation purposes
  noCursor();
  // Show new slide every 17 seconds
  getRandomSlide();
  setInterval(getRandomSlide, 17000);
}

function draw() {
  background(0);
  if (displayImage) {
    // Calculate aspect ratio
    let aspectRatio = displayImage.width / displayImage.height;
    // Calculate scaled width based on windowWidth
    let scaledWidth = windowWidth;
    let scaledHeight = windowWidth / aspectRatio;
    // Check if scaled height exceeds windowHeight
    if (scaledHeight > windowHeight) {
      scaledHeight = windowHeight;
      scaledWidth = windowHeight * aspectRatio;
    }
    // Show Image
    push();
    imageMode(CENTER);
    let a = (windowWidth - windowHeight) / 2;
    let y = windowHeight;
    let new_x = a + a + (y / 2); // Aligning image to right
    image(displayImage, new_x, height / 2, scaledWidth, scaledHeight);
    pop()

    // Show Headline
    let currentString = displayHeadline.substring(0, currentCharacter);
    push();
    textFont(displayFont); // Font
    textAlign(LEFT, TOP);
    textWrap(WORD);
    fill(letterFill);// Color of letters
    stroke(strokeFill); // Color of highlight
    strokeWeight(strokeThickness); // Thickness of highlight - 10 was good
    textSize(displaySize); // Size of letters
    let new_lol = a + a + (y / 3);
    text(currentString, headline_padding, headline_padding, new_lol - headline_padding);
    pop();
    currentCharacter += random(0.1,0.6);

    // Show Location
    push();
    textSize(35);
    textAlign(LEFT, BOTTOM);
    fill(255);
    stroke(0, 0, 0); 
    strokeWeight(3);
    textFont('Ubuntu Condensed');
    let location_padding_x = windowWidth * 0.11; // Calculate padding based on windowWidth and windowHeight
    let location_padding_y = windowHeight * 0.11;
    text(displayLocation, headline_padding, windowHeight - location_padding_y);
    pop();
  }
}

function getRandomSlide() {
  let table;
  // Alternate between good and bad headlines
  if (lastHeadlineMood == 'good') {
    table = good_place_bad_headline_table;
    lastHeadlineMood = 'bad';
  } else {
    table = bad_place_good_headline_table;
    lastHeadlineMood = 'good';
  }

  // Get random row from worksheet. 
  const randomRowIndex = Math.floor(random(1, table.getRowCount())); // Skip header row
  const row = table.getRow(randomRowIndex);
  const imagePath = row.get(6);
  // Store image and headline details
  displayHeadline = row.get(8);
  headlineType = row.get(7);
  stateFull = getStateFullName(row.get(2));
  countyName = row.get(3); //.toUpperCase();
  displayLocation = `${countyName}, ${stateFull}`;
  displayFont = random(fonts);
  print(displayFont);
  displaySize = random(85, 100); // random(73, 85);
  headline_padding = random(windowWidth * 0.07, windowWidth * 0.09); // to 0.05 to 0.08
  currentCharacter = 0;
  strokeThickness = random(9.5, 10.5);
  findingColors(headlineType);
  // Load Image
  loadImage(`/images/${imagePath}`, (img) => {
    displayImage = img;
  });
}

function findingColors(headlineType) {

  if (headlineType === 'Bad') {
    // If headlineType is 'bad', choose letter fill color from red, white, or blue color families
    let colorFamily = random(['red', 'white', 'blue']);

    // Choose stroke fill color - red must be one of the two colors
    if (colorFamily == 'white') {
      strokeFamily = "red";
    }
    else if (colorFamily == 'blue') {
      strokeFamily = "red";
    }
    else {
      strokeFamily = random(['blue', 'white']);
    }
    letterFill = generateColorFromFamily(colorFamily);
    
    strokeFill = generateColorFromFamily(strokeFamily);
    print(colorFamily, strokeFamily);
  } else {
    // If headlineType is not 'bad', choose letter fill color from pastel green, pink, yellow, purple, or blue
    let colorFamily = random(['green', 'pink', 'yellow', 'purple', 'pastel blue']);
    letterFill = generateColorFromFamily(colorFamily);

    // Choose stroke fill color from the remaining color families
    let remainingFamilies = ['green', 'pink', 'yellow', 'purple', 'pastel blue'].filter(family => family !== colorFamily);
    if (colorFamily == 'green') {
      remainingFamilies = ['pink', 'purple'];
    }
    if (colorFamily == 'pastel blue') {
      remainingFamilies = ['pink', 'yellow'];
    }
    if (colorFamily == 'yellow') {
      remainingFamilies = ['pink', 'purple', 'pastel blue'];
    }
    if (colorFamily == 'pink') {
      remainingFamilies = ['green', 'yellow', 'pastel blue'];
    }
    if (colorFamily == 'purple') {
      remainingFamilies = ['green', 'yellow'];
    }

    let strokeFamily = random(remainingFamilies);
    strokeFill = generateColorFromFamily(strokeFamily);
    print(colorFamily, strokeFamily);
  }
}

function generateColorFromFamily(colorFamily) {
  switch (colorFamily) {
    case 'red':
      return color(random(200, 256), random(0, 50), random(0, 50)); 
    case 'white':
      return color(random(240, 256)); 
    case 'blue':
      return color(random(0, 50), random(0, 50), random(200, 256)); 
    case 'green':
      return color(random(0, 150), random(207, 256), random(0, 150)); 
    case 'pink':
      return color(random(200,255), random(100, 200), random(100, 200)); 
    case 'yellow':
      return color(random(200,255), random(200,255), random(0, 150)); 
    case 'purple':
      return color(random(100, 240), random(0, 180), random(230, 240)); 
    case 'pastel blue':
      return color(random(0, 165), random(200, 256), random(200, 256)); 
    default:
      return color(255); 
  }
}

function windowResized() {
  resizeCanvas(windowWidth, windowHeight);
}


