// Global state
let robotCount = 0;
let robots = [];
let animationRunning = false;

// Section navigation
function showSection(sectionId) {
    // Hide all sections
    document.querySelectorAll('.content-section').forEach(section => {
        section.classList.remove('active');
    });

    // Remove active from all tabs
    document.querySelectorAll('.tab-button').forEach(button => {
        button.classList.remove('active');
    });

    // Show selected section
    document.getElementById(sectionId).classList.add('active');

    // Mark tab as active
    event.target.classList.add('active');
}

// Demo start - animate the magic box
function startDemo() {
    const box = document.querySelector('.magic-box');
    const heroAnimation = document.getElementById('heroAnimation');

    // Explode animation
    box.style.transform = 'scale(0.5)';

    setTimeout(() => {
        // Create robots coming out
        for (let i = 0; i < 5; i++) {
            setTimeout(() => {
                createFlyingRobot(heroAnimation);
            }, i * 200);
        }
    }, 300);

    setTimeout(() => {
        box.style.transform = 'scale(1)';
    }, 2000);
}

function createFlyingRobot(container) {
    const robot = document.createElement('div');
    robot.className = 'robot';
    robot.textContent = '🤖';
    robot.style.position = 'absolute';
    robot.style.left = '50%';
    robot.style.top = '50%';

    container.appendChild(robot);

    // Random direction
    const angle = Math.random() * Math.PI * 2;
    const distance = 100 + Math.random() * 100;
    const targetX = Math.cos(angle) * distance;
    const targetY = Math.sin(angle) * distance;

    robot.style.transition = 'all 1s ease-out';
    setTimeout(() => {
        robot.style.transform = `translate(${targetX}px, ${targetY}px) scale(0.5)`;
        robot.style.opacity = '0';
    }, 100);

    setTimeout(() => {
        robot.remove();
    }, 1200);
}

// Chain reaction visualization
function startChainReaction() {
    if (animationRunning) return;

    animationRunning = true;
    const container = document.getElementById('chainVisualization');

    // Reset
    container.innerHTML = '';
    robots = [];
    robotCount = 0;

    // Create Genesis Prime
    const genesis = createRobot(container, '🤖', 'Genesis Prime', 400, 50, 0);

    // Start spawning children
    setTimeout(() => spawnChildren(genesis, container, 1), 1000);
}

function createRobot(container, emoji, label, x, y, generation) {
    const robot = document.createElement('div');
    robot.className = 'robot';
    robot.textContent = emoji;
    robot.style.left = x + 'px';
    robot.style.top = y + 'px';

    // Add generation-specific styling
    const hue = (generation * 30) % 360;
    robot.style.background = `linear-gradient(135deg, hsl(${hue}, 70%, 60%), hsl(${hue + 30}, 70%, 50%))`;

    // Add label
    const labelDiv = document.createElement('div');
    labelDiv.className = 'robot-label';
    labelDiv.textContent = label;
    robot.appendChild(labelDiv);

    container.appendChild(robot);

    robotCount++;
    updateRobotCount();

    const robotData = { element: robot, x, y, generation, emoji, label };
    robots.push(robotData);

    return robotData;
}

function drawConnectionLine(container, fromRobot, toRobot) {
    const line = document.createElement('div');
    line.className = 'connection-line';

    const dx = toRobot.x - fromRobot.x;
    const dy = toRobot.y - fromRobot.y;
    const length = Math.sqrt(dx * dx + dy * dy);
    const angle = Math.atan2(dy, dx) * 180 / Math.PI;

    line.style.width = length + 'px';
    line.style.left = (fromRobot.x + 30) + 'px';
    line.style.top = (fromRobot.y + 30) + 'px';
    line.style.transform = `rotate(${angle}deg)`;

    container.appendChild(line);
}

function spawnChildren(parentRobot, container, generation) {
    if (generation > 3 || robotCount > 30) {
        animationRunning = false;
        return;
    }

    const numChildren = generation === 1 ? 3 : 2;
    const childEmojis = ['🔧', '🏗️', '🔨', '✅', '📝', '🧪'];
    const childLabels = ['Analyzer', 'Architect', 'Builder', 'Validator', 'Documenter', 'Tester'];

    for (let i = 0; i < numChildren; i++) {
        setTimeout(() => {
            // Calculate position
            const angle = (Math.PI / (numChildren + 1)) * (i + 1) - Math.PI / 2;
            const distance = 150;
            const childX = parentRobot.x + Math.cos(angle) * distance + (generation * 100) - 50;
            const childY = parentRobot.y + Math.sin(angle) * distance + (generation * 100);

            const childIndex = (generation * 3 + i) % childEmojis.length;
            const childEmoji = childEmojis[childIndex];
            const childLabel = childLabels[childIndex];

            const childRobot = createRobot(
                container,
                childEmoji,
                childLabel,
                childX,
                childY,
                generation
            );

            // Draw connection line
            drawConnectionLine(container, parentRobot, childRobot);

            // Spawn grandchildren
            if (generation < 3 && robotCount < 25) {
                setTimeout(() => {
                    spawnChildren(childRobot, container, generation + 1);
                }, 1000);
            }
        }, i * 500);
    }
}

function updateRobotCount() {
    document.getElementById('robotCount').textContent = robotCount;

    // Animate the counter
    const counter = document.getElementById('robotCount');
    counter.style.transform = 'scale(1.3)';
    setTimeout(() => {
        counter.style.transform = 'scale(1)';
    }, 200);
}

function resetChainReaction() {
    const container = document.getElementById('chainVisualization');
    container.innerHTML = '';
    robots = [];
    robotCount = 0;
    updateRobotCount();
    animationRunning = false;
}

// Example switching
function showExample(exampleId) {
    // Hide all example cards
    document.querySelectorAll('.example-card').forEach(card => {
        card.classList.remove('active');
    });

    // Remove active from all buttons
    document.querySelectorAll('.example-btn').forEach(btn => {
        btn.classList.remove('active');
    });

    // Show selected example
    document.getElementById('example-' + exampleId).classList.add('active');

    // Mark button as active
    event.target.classList.add('active');
}

// Auto-start chain reaction when entering that section
document.addEventListener('DOMContentLoaded', () => {
    // Initialize robot count
    updateRobotCount();

    // Add observer to auto-start chain reaction when section becomes visible
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting && entry.target.id === 'chain') {
                // Auto-start once when section becomes visible
                if (robotCount === 0) {
                    setTimeout(() => {
                        if (!animationRunning) {
                            startChainReaction();
                        }
                    }, 500);
                }
            }
        });
    }, { threshold: 0.5 });

    const chainSection = document.getElementById('chain');
    if (chainSection) {
        observer.observe(chainSection);
    }

    // Add hover effects to robots in examples
    document.querySelectorAll('.robot').forEach(robot => {
        robot.addEventListener('mouseenter', function() {
            this.style.animation = 'bounce 0.5s ease';
        });

        robot.addEventListener('animationend', function() {
            this.style.animation = '';
        });
    });

    // Add parallax effect to hero
    document.addEventListener('mousemove', (e) => {
        const magicBox = document.querySelector('.magic-box');
        if (magicBox) {
            const xAxis = (window.innerWidth / 2 - e.pageX) / 25;
            const yAxis = (window.innerHeight / 2 - e.pageY) / 25;
            magicBox.style.transform = `rotateY(${xAxis}deg) rotateX(${yAxis}deg)`;
        }
    });

    // Animate elements on scroll
    const animateOnScroll = () => {
        const elements = document.querySelectorAll('.card, .possibility-card, .example-card');

        elements.forEach(element => {
            const elementTop = element.getBoundingClientRect().top;
            const elementBottom = element.getBoundingClientRect().bottom;

            if (elementTop < window.innerHeight && elementBottom > 0) {
                element.style.opacity = '1';
                element.style.transform = 'translateY(0)';
            }
        });
    };

    // Initial setup for scroll animation
    document.querySelectorAll('.card, .possibility-card').forEach(element => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(30px)';
        element.style.transition = 'all 0.6s ease';
    });

    window.addEventListener('scroll', animateOnScroll);
    animateOnScroll(); // Initial check

    // Add click effect to magic box
    const magicBox = document.querySelector('.magic-box');
    if (magicBox) {
        magicBox.addEventListener('click', () => {
            startDemo();
        });
    }
});

// Add robot clicking in chain visualization
document.addEventListener('click', (e) => {
    if (e.target.classList.contains('robot') && e.target.closest('#chainVisualization')) {
        const robot = e.target;

        // Create sparkle effect
        for (let i = 0; i < 8; i++) {
            setTimeout(() => {
                const sparkle = document.createElement('div');
                sparkle.textContent = '✨';
                sparkle.style.position = 'absolute';
                sparkle.style.left = robot.offsetLeft + 30 + 'px';
                sparkle.style.top = robot.offsetTop + 30 + 'px';
                sparkle.style.pointerEvents = 'none';
                sparkle.style.transition = 'all 1s ease-out';

                document.getElementById('chainVisualization').appendChild(sparkle);

                const angle = (Math.PI * 2 / 8) * i;
                const distance = 50;

                setTimeout(() => {
                    sparkle.style.transform = `translate(${Math.cos(angle) * distance}px, ${Math.sin(angle) * distance}px) scale(0)`;
                    sparkle.style.opacity = '0';
                }, 50);

                setTimeout(() => sparkle.remove(), 1100);
            }, i * 50);
        }
    }
});

// Add keyboard shortcuts
document.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowRight') {
        const sections = ['intro', 'chain', 'examples', 'possibilities'];
        const activeSection = document.querySelector('.content-section.active');
        const currentIndex = sections.indexOf(activeSection.id);
        const nextIndex = (currentIndex + 1) % sections.length;

        const nextButton = document.querySelectorAll('.tab-button')[nextIndex];
        if (nextButton) nextButton.click();
    }

    if (e.key === 'ArrowLeft') {
        const sections = ['intro', 'chain', 'examples', 'possibilities'];
        const activeSection = document.querySelector('.content-section.active');
        const currentIndex = sections.indexOf(activeSection.id);
        const prevIndex = (currentIndex - 1 + sections.length) % sections.length;

        const prevButton = document.querySelectorAll('.tab-button')[prevIndex];
        if (prevButton) prevButton.click();
    }

    if (e.key === ' ' && document.querySelector('#chain.active')) {
        e.preventDefault();
        if (animationRunning) {
            resetChainReaction();
        } else {
            startChainReaction();
        }
    }
});

// Add touch support for mobile
let touchStartX = 0;
let touchEndX = 0;

document.addEventListener('touchstart', e => {
    touchStartX = e.changedTouches[0].screenX;
});

document.addEventListener('touchend', e => {
    touchEndX = e.changedTouches[0].screenX;
    handleSwipe();
});

function handleSwipe() {
    const swipeThreshold = 50;
    const diff = touchStartX - touchEndX;

    if (Math.abs(diff) > swipeThreshold) {
        if (diff > 0) {
            // Swipe left - next section
            const event = new KeyboardEvent('keydown', { key: 'ArrowRight' });
            document.dispatchEvent(event);
        } else {
            // Swipe right - previous section
            const event = new KeyboardEvent('keydown', { key: 'ArrowLeft' });
            document.dispatchEvent(event);
        }
    }
}

// Easter egg - konami code
let konamiCode = [];
const konamiSequence = ['ArrowUp', 'ArrowUp', 'ArrowDown', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'ArrowLeft', 'ArrowRight', 'b', 'a'];

document.addEventListener('keydown', (e) => {
    konamiCode.push(e.key);
    konamiCode = konamiCode.slice(-10);

    if (konamiCode.join(',') === konamiSequence.join(',')) {
        activateEasterEgg();
        konamiCode = [];
    }
});

function activateEasterEgg() {
    const body = document.body;
    body.style.animation = 'rainbow 2s linear infinite';

    // Add rainbow animation
    const style = document.createElement('style');
    style.textContent = `
        @keyframes rainbow {
            0% { filter: hue-rotate(0deg); }
            100% { filter: hue-rotate(360deg); }
        }
    `;
    document.head.appendChild(style);

    // Create robot rain
    for (let i = 0; i < 30; i++) {
        setTimeout(() => {
            const robot = document.createElement('div');
            robot.textContent = '🤖';
            robot.style.position = 'fixed';
            robot.style.left = Math.random() * window.innerWidth + 'px';
            robot.style.top = '-50px';
            robot.style.fontSize = '2rem';
            robot.style.zIndex = '9999';
            robot.style.pointerEvents = 'none';
            robot.style.transition = 'all 3s linear';

            document.body.appendChild(robot);

            setTimeout(() => {
                robot.style.top = window.innerHeight + 'px';
                robot.style.transform = 'rotate(720deg)';
            }, 100);

            setTimeout(() => robot.remove(), 3200);
        }, i * 100);
    }

    setTimeout(() => {
        body.style.animation = '';
        style.remove();
    }, 5000);
}
