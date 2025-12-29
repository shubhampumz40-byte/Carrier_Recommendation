// Main application JavaScript

// Global variables
let personalityData = null;

// Load personality data from localStorage if available
document.addEventListener('DOMContentLoaded', function() {
    const stored = localStorage.getItem('personalityResult');
    if (stored) {
        personalityData = JSON.parse(stored);
    }
});

// Utility functions
function showLoading(element, text = 'Loading...') {
    element.innerHTML = `<i class="fas fa-spinner fa-spin me-2"></i>${text}`;
    element.disabled = true;
    element.classList.add('loading');
}

function hideLoading(element, originalText) {
    element.innerHTML = originalText;
    element.disabled = false;
    element.classList.remove('loading');
}

function showToast(message, type = 'info') {
    // Create toast element
    const toast = document.createElement('div');
    toast.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    toast.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    toast.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(toast);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (toast.parentNode) {
            toast.parentNode.removeChild(toast);
        }
    }, 5000);
}

// Career recommendation functions
async function getCareerRecommendations(data) {
    try {
        const response = await fetch('/api/recommend', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        if (!response.ok) {
            throw new Error('Failed to get recommendations');
        }
        
        return await response.json();
    } catch (error) {
        console.error('Error getting recommendations:', error);
        throw error;
    }
}

// Visualization functions
function createCareerNetwork(data, containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;
    
    // Simple network visualization using D3.js concepts with vanilla JS
    const width = container.offsetWidth;
    const height = 400;
    
    // Create SVG
    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('width', width);
    svg.setAttribute('height', height);
    svg.style.border = '1px solid #ddd';
    svg.style.borderRadius = '5px';
    
    container.appendChild(svg);
    
    // Add nodes and connections (simplified)
    const centerX = width / 2;
    const centerY = height / 2;
    
    // User node (center)
    const userCircle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    userCircle.setAttribute('cx', centerX);
    userCircle.setAttribute('cy', centerY);
    userCircle.setAttribute('r', 30);
    userCircle.setAttribute('fill', '#0d6efd');
    svg.appendChild(userCircle);
    
    // User label
    const userText = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    userText.setAttribute('x', centerX);
    userText.setAttribute('y', centerY + 5);
    userText.setAttribute('text-anchor', 'middle');
    userText.setAttribute('fill', 'white');
    userText.setAttribute('font-weight', 'bold');
    userText.textContent = 'You';
    svg.appendChild(userText);
    
    // Career nodes (around the center)
    if (data.nodes) {
        const careerNodes = data.nodes.filter(n => n.type === 'career');
        const angleStep = (2 * Math.PI) / careerNodes.length;
        
        careerNodes.forEach((node, index) => {
            const angle = index * angleStep;
            const radius = 120;
            const x = centerX + Math.cos(angle) * radius;
            const y = centerY + Math.sin(angle) * radius;
            
            // Career circle
            const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
            circle.setAttribute('cx', x);
            circle.setAttribute('cy', y);
            circle.setAttribute('r', 20);
            circle.setAttribute('fill', '#198754');
            svg.appendChild(circle);
            
            // Connection line
            const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
            line.setAttribute('x1', centerX);
            line.setAttribute('y1', centerY);
            line.setAttribute('x2', x);
            line.setAttribute('y2', y);
            line.setAttribute('stroke', '#6c757d');
            line.setAttribute('stroke-width', 2);
            svg.insertBefore(line, userCircle);
            
            // Career label
            const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
            text.setAttribute('x', x);
            text.setAttribute('y', y - 30);
            text.setAttribute('text-anchor', 'middle');
            text.setAttribute('font-size', '12');
            text.setAttribute('font-weight', 'bold');
            text.textContent = node.name;
            svg.appendChild(text);
        });
    }
}

function createSkillsRadar(skills, containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;
    
    // Create a simple radar chart representation
    const skillsData = skills.map(skill => ({
        skill: skill,
        level: Math.random() * 5 + 1 // Random level for demo
    }));
    
    // Use Chart.js for radar chart
    const canvas = document.createElement('canvas');
    container.appendChild(canvas);
    
    new Chart(canvas, {
        type: 'radar',
        data: {
            labels: skillsData.map(s => s.skill),
            datasets: [{
                label: 'Your Skills',
                data: skillsData.map(s => s.level),
                backgroundColor: 'rgba(13, 110, 253, 0.2)',
                borderColor: 'rgba(13, 110, 253, 1)',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            scales: {
                r: {
                    beginAtZero: true,
                    max: 5
                }
            }
        }
    });
}

// Form validation
function validateAssessmentForm(formData) {
    const interests = formData.getAll('interests');
    const skills = formData.getAll('skills');
    const subjects = formData.getAll('subjects');
    
    if (interests.length === 0) {
        showToast('Please select at least one interest.', 'warning');
        return false;
    }
    
    if (skills.length === 0) {
        showToast('Please select at least one skill.', 'warning');
        return false;
    }
    
    if (subjects.length === 0) {
        showToast('Please select at least one subject.', 'warning');
        return false;
    }
    
    return true;
}

// Export functions for global use
window.CareerRecommender = {
    getRecommendations: getCareerRecommendations,
    createNetwork: createCareerNetwork,
    createRadar: createSkillsRadar,
    validateForm: validateAssessmentForm,
    showToast: showToast
};