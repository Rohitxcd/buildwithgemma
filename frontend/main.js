// DOM Elements
const dropZone = document.getElementById('drop-zone');
const fileInput = document.getElementById('file-input');
const previewContainer = document.getElementById('preview-container');
const imagePreview = document.getElementById('image-preview');
const removeBtn = document.getElementById('remove-btn');
const processBtn = document.getElementById('process-btn');

const uploadSection = document.getElementById('upload-section');
const loadingSection = document.getElementById('loading-section');
const loadingStatus = document.getElementById('loading-status');
const resultsSection = document.getElementById('results-section');

// Loading steps
const steps = {
  upload: document.getElementById('step-upload'),
  analyze: document.getElementById('step-analyze'),
  protect: document.getElementById('step-protect'),
  verify: document.getElementById('step-verify'),
};

// Results elements
const originalImage = document.getElementById('original-image');
const protectedImage = document.getElementById('protected-image');
const downloadBtn = document.getElementById('download-btn');
const newUploadBtn = document.getElementById('new-upload-btn');

// View toggle
const btnSideBySide = document.getElementById('btn-side-by-side');
const btnSlider = document.getElementById('btn-slider');
const comparisonDisplay = document.getElementById('comparison-display');
const sliderWrapper = document.getElementById('slider-wrapper');

// Slider elements
const sliderOriginal = document.getElementById('slider-original');
const sliderProtected = document.getElementById('slider-protected');
const sliderResize = document.getElementById('slider-resize');
const sliderHandle = document.getElementById('slider-handle');

// Analytics dashboard elements
const gaugeBefore = document.getElementById('gauge-before');
const gaugeAfter = document.getElementById('gauge-after');
const valBefore = document.getElementById('val-before');
const valAfter = document.getElementById('val-after');
const summaryBeforeText = document.getElementById('summary-before-text');
const summaryAfterText = document.getElementById('summary-after-text');

const detailLandmark = document.getElementById('detail-landmark');
const detailFrequency = document.getElementById('detail-frequency');
const detailTexture = document.getElementById('detail-texture');
const detailBody = document.getElementById('detail-body');
const strengthTag = document.getElementById('strength-tag');

const checkIdentifiable = document.getElementById('check-identifiable');
const checkImproved = document.getElementById('check-improved');
const txtIdentifiable = document.getElementById('txt-identifiable');
const txtImproved = document.getElementById('txt-improved');

const risksList = document.getElementById('risks-list');
const recsList = document.getElementById('recs-list');

const metaFilename = document.getElementById('meta-filename');
const metaDims = document.getElementById('meta-dims');
const metaFaces = document.getElementById('meta-faces');
const metaFaceBox = document.getElementById('meta-face-box');
const metaBodyBox = document.getElementById('meta-body-box');
const metaBodyProtected = document.getElementById('meta-body-protected');
const metaPipelineTags = document.getElementById('meta-pipeline-tags');

// State
let selectedFile = null;
let loadingInterval = null;

// Helpers
const getFileName = (pathStr) => {
  if (!pathStr) return '';
  const parts = pathStr.split(/[\\/]/);
  return parts[parts.length - 1];
};

// Event Listeners for Upload Flow
dropZone.addEventListener('click', () => fileInput.click());

dropZone.addEventListener('dragover', (e) => {
  e.preventDefault();
  dropZone.classList.add('dragover');
});

dropZone.addEventListener('dragleave', () => {
  dropZone.classList.remove('dragover');
});

dropZone.addEventListener('drop', (e) => {
  e.preventDefault();
  dropZone.classList.remove('dragover');
  if (e.dataTransfer.files.length > 0) {
    handleFileSelect(e.dataTransfer.files[0]);
  }
});

fileInput.addEventListener('change', (e) => {
  if (e.target.files.length > 0) {
    handleFileSelect(e.target.files[0]);
  }
});

removeBtn.addEventListener('click', () => {
  selectedFile = null;
  fileInput.value = '';
  imagePreview.src = '';
  previewContainer.classList.add('hidden');
  dropZone.classList.remove('hidden');
});

function handleFileSelect(file) {
  if (!file.type.startsWith('image/')) {
    alert('Please upload an image file.');
    return;
  }
  selectedFile = file;
  const reader = new FileReader();
  reader.onload = (e) => {
    imagePreview.src = e.target.result;
    dropZone.classList.add('hidden');
    previewContainer.classList.remove('hidden');
  };
  reader.readAsDataURL(file);
}

// Processing Execution
processBtn.addEventListener('click', async () => {
  if (!selectedFile) return;

  // Toggle UI visibility
  uploadSection.classList.add('hidden');
  loadingSection.classList.remove('hidden');
  resetLoadingSteps();

  // Simulated sequential steps progress
  let step = 1;
  loadingStatus.textContent = "Uploading image to server...";
  setActiveStep('upload');

  loadingInterval = setInterval(() => {
    if (step === 1) {
      setStepCompleted('upload');
      setActiveStep('analyze');
      loadingStatus.textContent = "Gemma performing privacy risk analysis...";
      step = 2;
    } else if (step === 2) {
      setStepCompleted('analyze');
      setActiveStep('protect');
      loadingStatus.textContent = "Applying computer vision protection transformations...";
      step = 3;
    } else if (step === 3) {
      setStepCompleted('protect');
      setActiveStep('verify');
      loadingStatus.textContent = "Gemma performing post-protection verification...";
      step = 4;
    }
  }, 2200);

  const formData = new FormData();
  formData.append('file', selectedFile);

  try {
    const response = await fetch('/protect/', {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Failed to process image');
    }

    const data = await response.json();
    clearInterval(loadingInterval);
    
    // Complete all steps in UI
    setStepCompleted('upload');
    setStepCompleted('analyze');
    setStepCompleted('protect');
    setStepCompleted('verify');
    loadingStatus.textContent = "Finished processing!";

    setTimeout(() => {
      loadingSection.classList.add('hidden');
      displayResults(data);
    }, 500);

  } catch (error) {
    clearInterval(loadingInterval);
    alert(`Error: ${error.message}`);
    loadingSection.classList.add('hidden');
    uploadSection.classList.remove('hidden');
  }
});

// Loading state UI helpers
function resetLoadingSteps() {
  Object.keys(steps).forEach(key => {
    steps[key].className = 'step';
  });
}

function setActiveStep(stepKey) {
  steps[stepKey].classList.add('active');
}

function setStepCompleted(stepKey) {
  steps[stepKey].classList.remove('active');
  steps[stepKey].classList.add('completed');
}

// Display results in Dashboard
function displayResults(data) {
  resultsSection.classList.remove('hidden');

  // Setup Image Sources (extracting filename via helper)
  const origFileName = getFileName(data.metadata.original_image);
  const protFileName = getFileName(data.protected_image);
  
  const originalUrl = `/uploads/${origFileName}`;
  const protectedUrl = `/protected/${protFileName}`;

  originalImage.src = originalUrl;
  protectedImage.src = protectedUrl;
  downloadBtn.href = protectedUrl;

  // Setup Slider Images
  sliderOriginal.src = originalUrl;
  sliderProtected.src = protectedUrl;
  
  // Reset slider position to 50%
  sliderResize.style.width = '50%';
  sliderHandle.style.left = '50%';

  // Risk Gauges
  const beforeScore = data.before_protection.risk_score || 0;
  const afterScore = data.after_protection.risk_score || 0;

  valBefore.textContent = `${beforeScore}%`;
  valAfter.textContent = `${afterScore}%`;

  // Draw ring gradients based on scores
  gaugeBefore.style.background = `conic-gradient(var(--danger) 0% ${beforeScore}%, rgba(255, 255, 255, 0.04) ${beforeScore}% 100%)`;
  gaugeAfter.style.background = `conic-gradient(var(--success) 0% ${afterScore}%, rgba(255, 255, 255, 0.04) ${afterScore}% 100%)`;

  summaryBeforeText.textContent = `${data.before_protection.risk_level} Risk - ${data.before_protection.summary}`;
  summaryAfterText.textContent = `${data.after_protection.risk_level} Risk - ${data.after_protection.summary}`;

  // Strategy Details Toggles
  toggleStrategyActive(detailLandmark, data.strategy_used.landmark_perturbation);
  toggleStrategyActive(detailFrequency, data.strategy_used.frequency_mask);
  toggleStrategyActive(detailTexture, data.strategy_used.texture_shift);
  toggleStrategyActive(detailBody, data.strategy_used.body_region_protection);

  // Strategy Strength Badge
  strengthTag.textContent = data.strategy_used.strength;
  strengthTag.className = 'badge';
  if (data.strategy_used.strength === 'high') {
    strengthTag.style.background = 'var(--danger)';
  } else if (data.strategy_used.strength === 'low') {
    strengthTag.style.background = 'var(--primary)';
  } else {
    strengthTag.style.background = 'var(--warning)';
  }

  // Gemma AI Verification Panel
  const isIdentifiable = data.after_protection.face_still_identifiable;
  const isImproved = data.after_protection.privacy_improved;

  if (isIdentifiable === true) {
    checkIdentifiable.className = 'check-item compromised';
    txtIdentifiable.textContent = 'Yes (Compromised)';
    checkIdentifiable.querySelector('.check-icon').textContent = '⚠️';
  } else if (isIdentifiable === false) {
    checkIdentifiable.className = 'check-item secured';
    txtIdentifiable.textContent = 'No (Secured)';
    checkIdentifiable.querySelector('.check-icon').textContent = '✅';
  } else {
    checkIdentifiable.className = 'check-item';
    txtIdentifiable.textContent = 'Indeterminate';
    checkIdentifiable.querySelector('.check-icon').textContent = '❓';
  }

  if (isImproved === true) {
    checkImproved.className = 'check-item secured';
    txtImproved.textContent = 'Yes';
    checkImproved.querySelector('.check-icon').textContent = '✅';
  } else if (isImproved === false) {
    checkImproved.className = 'check-item compromised';
    txtImproved.textContent = 'No';
    checkImproved.querySelector('.check-icon').textContent = '⚠️';
  } else {
    checkImproved.className = 'check-item';
    txtImproved.textContent = 'No Change';
    checkImproved.querySelector('.check-icon').textContent = '❓';
  }

  // Populating Lists
  populateList(risksList, data.after_protection.remaining_risks || []);
  populateList(recsList, data.after_protection.recommendations || []);

  // Diagnostic Table
  metaFilename.textContent = data.metadata.original_filename || 'Unknown';
  metaDims.textContent = `${data.metadata.image_width || 0} x ${data.metadata.image_height || 0} px`;
  metaFaces.textContent = data.metadata.faces_detected || 0;
  metaFaceBox.textContent = formatRegion(data.metadata.face_region);
  metaBodyBox.textContent = formatRegion(data.metadata.body_region);
  metaBodyProtected.textContent = data.metadata.body_protected ? 'Yes (CV Segmented)' : 'No';

  // Pipeline tags
  metaPipelineTags.innerHTML = '';
  if (data.metadata.operations_applied && data.metadata.operations_applied.length > 0) {
    data.metadata.operations_applied.forEach(op => {
      const span = document.createElement('span');
      span.className = 'pipeline-tag';
      span.textContent = op;
      metaPipelineTags.appendChild(span);
    });
  } else {
    metaPipelineTags.innerHTML = '<span class="text-muted">None</span>';
  }
}

function toggleStrategyActive(element, isActive) {
  if (isActive) {
    element.classList.add('active');
  } else {
    element.classList.remove('active');
  }
}

function formatRegion(region) {
  if (!region || region.length !== 4) return 'None';
  return `[${region[0]}, ${region[1]}, ${region[2]}, ${region[3]}]`;
}

function populateList(element, items) {
  element.innerHTML = '';
  if (items.length === 0) {
    element.innerHTML = '<li>None identified</li>';
    return;
  }
  items.forEach(item => {
    const li = document.createElement('li');
    li.textContent = item;
    element.appendChild(li);
  });
}

// Side-by-Side vs Slider Toggle
btnSideBySide.addEventListener('click', () => {
  btnSideBySide.classList.add('active');
  btnSlider.classList.remove('active');
  comparisonDisplay.classList.add('side-by-side');
  sliderWrapper.classList.add('hidden');
  document.querySelectorAll('.image-box').forEach(box => box.classList.remove('hidden'));
});

btnSlider.addEventListener('click', () => {
  btnSlider.classList.add('active');
  btnSideBySide.classList.remove('active');
  comparisonDisplay.classList.remove('side-by-side');
  sliderWrapper.classList.remove('hidden');
  document.querySelectorAll('.image-box').forEach(box => box.classList.add('hidden'));
  
  // Set equal sizes initially
  adjustSliderImageSizes();
});

// Slider comparison interaction logic
let isDragging = false;

sliderHandle.addEventListener('mousedown', (e) => {
  isDragging = true;
  e.preventDefault();
});

window.addEventListener('mouseup', () => {
  isDragging = false;
});

window.addEventListener('mousemove', (e) => {
  if (!isDragging) return;
  moveSlider(e.clientX);
});

// Touch support for slider
sliderHandle.addEventListener('touchstart', (e) => {
  isDragging = true;
  e.preventDefault();
});

window.addEventListener('touchend', () => {
  isDragging = false;
});

window.addEventListener('touchmove', (e) => {
  if (!isDragging) return;
  if (e.touches.length > 0) {
    moveSlider(e.touches[0].clientX);
  }
});

function moveSlider(clientX) {
  const containerRect = sliderWrapper.querySelector('.slider-image-container').getBoundingClientRect();
  let offsetX = clientX - containerRect.left;
  
  // Clamp values
  if (offsetX < 0) offsetX = 0;
  if (offsetX > containerRect.width) offsetX = containerRect.width;

  const percentage = (offsetX / containerRect.width) * 100;
  
  sliderResize.style.width = `${percentage}%`;
  sliderHandle.style.left = `${percentage}%`;
}

function adjustSliderImageSizes() {
  const container = sliderWrapper.querySelector('.slider-image-container');
  const originalWidth = sliderOriginal.clientWidth;
  
  // Make sure the absolute positioned protected image matches the original image dimensions exactly
  sliderProtected.style.width = `${originalWidth}px`;
  sliderProtected.style.height = `${sliderOriginal.clientHeight}px`;
}

// Re-adjust size on window resize
window.addEventListener('resize', () => {
  if (btnSlider.classList.contains('active')) {
    adjustSliderImageSizes();
  }
});

// Reset for another upload
newUploadBtn.addEventListener('click', () => {
  selectedFile = null;
  fileInput.value = '';
  imagePreview.src = '';
  previewContainer.classList.add('hidden');
  resultsSection.classList.add('hidden');
  uploadSection.classList.remove('hidden');
  dropZone.classList.remove('hidden');
  
  // Reset buttons
  btnSideBySide.click();
});
