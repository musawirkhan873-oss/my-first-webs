// Main JavaScript functionality
document.addEventListener('DOMContentLoaded', function() {
    console.log('Website loaded successfully!');
    
    // Smooth scrolling for navigation links
    document.querySelectorAll('nav a').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Contact form handling
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            handleFormSubmission();
        });
    }

    // Initialize page
    initializePage();
});

// Search functionality
function searchContent() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    const sections = document.querySelectorAll('main section');
    let found = false;

    sections.forEach(section => {
        const text = section.textContent.toLowerCase();
        if (text.includes(searchTerm)) {
            section.scrollIntoView({ behavior: 'smooth' });
            section.style.backgroundColor = '#ffffcc';
            setTimeout(() => {
                section.style.backgroundColor = '';
            }, 2000);
            found = true;
        }
    });

    if (!found && searchTerm) {
        alert('No results found for: ' + searchTerm);
    }
}

// Handle contact form submission
function handleFormSubmission() {
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const message = document.getElementById('message').value;

    // Basic validation
    if (!name || !email || !message) {
        alert('Please fill in all fields');
        return;
    }

    // Create form data object
    const formData = {
        name: name,
        email: email,
        message: message,
        timestamp: new Date().toISOString()
    };

    // Send to backend (you'll need to implement the backend endpoint)
    sendToBackend(formData);
}

// Send data to Python backend
async function sendToBackend(formData) {
    try {
        const response = await fetch('http://localhost:5000/api/contact', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });

        if (response.ok) {
            const result = await response.json();
            alert('Message sent successfully!');
            document.getElementById('contactForm').reset();
        } else {
            alert('Error sending message. Please try again.');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Network error. Please check if the server is running.');
    }
}

// Load more courses (demo functionality)
function loadMoreCourses() {
    const coursesList = document.getElementById('coursesList');
    const additionalCourses = [
        'Artificial Intelligence',
        'Machine Learning',
        'Cyber Security',
        'Database Management',
        'Mobile App Development'
    ];

    additionalCourses.forEach(course => {
        const li = document.createElement('li');
        li.textContent = course;
        li.style.animation = 'fadeIn 0.5s ease-in';
        coursesList.appendChild(li);
    });

    // Disable button after loading all courses
    event.target.disabled = true;
    event.target.textContent = 'All Courses Loaded';
}

// Initialize page with some dynamic content
function initializePage() {
    // Add some interactive features
    addHoverEffects();
    setupScrollAnimations();
}

// Add hover effects to images
function addHoverEffects() {
    const images = document.querySelectorAll('img');
    images.forEach(img => {
        img.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.05)';
            this.style.transition = 'transform 0.3s ease';
        });
        
        img.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
        });
    });
}

// Setup scroll animations
function setupScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observe all sections
    document.querySelectorAll('main section').forEach(section => {
        section.style.opacity = '0';
        section.style.transform = 'translateY(20px)';
        section.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        observer.observe(section);
    });
}

// Utility function for making API calls
async function makeAPICall(url, method = 'GET', data = null) {
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
        }
    };

    if (data && (method === 'POST' || method === 'PUT')) {
        options.body = JSON.stringify(data);
    }

    try {
        const response = await fetch(url, options);
        return await response.json();
    } catch (error) {
        console.error('API call failed:', error);
        return null;
    }
}