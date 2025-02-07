const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

const centralCircle = document.getElementById('central-circle');
const container = document.querySelector('.container');

const colors = {
    "Popular on Social Media": { r: 0, g: 128, b: 0 },
    "Large Market Value": { r: 255, g: 165, b: 0 },
    "Easy to Buy/Sell": { r: 255, g: 0, b: 0 },
    "Stable Price": { r: 128, g: 128, b: 128 },
    "High Community Engagement": { r: 0, g: 0, b: 255 }
};

// Divider variables for scaling values
const mindshareDivisor = 0.1;
const marketCapDivisor = 1000000;
const liquidityDivisor = 50000;
const priceDivisor = 100;
const engagementsDivisor = 10;

const details = document.getElementById('details');
let selectedCrypto = null;
const useRandomValues = false; // Set this to false to use sliders

function showDetails(crypto) {
    selectedCrypto = crypto;
    details.style.display = 'block';
    updateDetails();
    if (!useRandomValues) {
        document.getElementById('sliders').style.display = 'block';
        document.getElementById('mindshare-slider').value = crypto.mindshare;
        document.getElementById('marketCap-slider').value = crypto.marketCap;
        document.getElementById('liquidity-slider').value = crypto.liquidity;
        document.getElementById('price-slider').value = crypto.price;
        document.getElementById('averageEngagementsCount-slider').value = crypto.averageEngagementsCount;
    }
}

function updateDetails() {
    if (selectedCrypto) {
        details.innerHTML = `
            <h2>${selectedCrypto.agentName}</h2>
            <p>Mindshare: ${(selectedCrypto.mindshare / mindshareDivisor).toFixed(2)}</p>
            <p>Market Cap: ${(selectedCrypto.marketCap / marketCapDivisor).toFixed(2)}</p>
            <p>Liquidity: ${(selectedCrypto.liquidity / liquidityDivisor).toFixed(2)}</p>
            <p>Price: ${(selectedCrypto.price / priceDivisor).toFixed(2)}</p>
            <p>Average Engagements Count: ${(selectedCrypto.averageEngagementsCount / engagementsDivisor).toFixed(2)}</p>
        `;
    }
}

if (!useRandomValues) {
    document.getElementById('sliders').addEventListener('submit', (e) => {
        e.preventDefault();
        const data = {
            name: selectedCrypto.agentName,
            mindshare: parseInt(document.getElementById('mindshare-slider').value) * mindshareDivisor,
            marketCap: parseInt(document.getElementById('marketCap-slider').value) * marketCapDivisor,
            liquidity: parseInt(document.getElementById('liquidity-slider').value) * liquidityDivisor,
            price: parseInt(document.getElementById('price-slider').value) * priceDivisor,
            averageEngagementsCount: parseInt(document.getElementById('averageEngagementsCount-slider').value) * engagementsDivisor
        };
        fetch('/update', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        }).then(response => response.json()).then(updatedCrypto => {
            selectedCrypto = updatedCrypto;
            updateDetails();
        });
    });
}

class Circle {
    constructor(crypto, region) {
        this.crypto = crypto;
        this.region = region;
        this.element = document.createElement('div');
        this.element.className = 'circle';
        this.element.style.backgroundColor = `rgb(${colors[region].r}, ${colors[region].g}, ${colors[region].b})`;
        this.element.innerText = crypto.agentName;
        container.appendChild(this.element);
        this.element.addEventListener('click', () => {
            showDetails(crypto);
        });
    }
    updatePosition(x, y) {
        this.element.style.left = `${x}px`;
        this.element.style.top = `${y}px`;
    }
}

class Particle {
    constructor(x, y, targetX, targetY, startColor, endColor) {
        this.x = x;
        this.y = y;
        this.targetX = targetX;
        this.targetY = targetY;
        this.vx = (targetX - x) * 0.005 + (Math.random() - 0.5) * 0.5;
        this.vy = (targetY - y) * 0.005 + (Math.random() - 0.5) * 0.5;
        this.alpha = 1;
        this.size = 1;
        this.angle = 0;
        this.amplitude = 1;
        this.startColor = startColor;
        this.endColor = endColor;
    }
    update() {
        this.x += this.vx;
        this.y += this.vy + Math.sin(this.angle) * this.amplitude;
        this.angle += 0.1;
        this.alpha -= 0.005;
        const dist = Math.hypot(this.x - this.targetX, this.y - this.targetY);
        if (dist < 5) {
            this.alpha = 0;
        }
    }
    draw() {
        const progress = 1 - this.alpha;
        const r = this.startColor.r + progress * (this.endColor.r - this.startColor.r);
        const g = this.startColor.g + progress * (this.endColor.g - this.startColor.g);
        const b = this.startColor.b + progress * (this.endColor.b - this.startColor.b);
        ctx.globalAlpha = this.alpha;
        ctx.fillStyle = `rgb(${r}, ${g}, ${b})`;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fill();
        ctx.globalAlpha = 1;
    }
}

const circles = {};
let particles = [];

function getHighestValueRegion(crypto) {
    const values = {
        "Popular on Social Media": crypto.mindshare / mindshareDivisor,
        "Large Market Value": crypto.marketCap / marketCapDivisor,
        "Easy to Buy/Sell": crypto.liquidity / liquidityDivisor,
        "Stable Price": crypto.price / priceDivisor,
        "High Community Engagement": crypto.averageEngagementsCount / engagementsDivisor
    };
    return Object.keys(values).reduce((a, b) => values[a] > values[b] ? a : b);
}

function getRegionPosition(region) {
    const width = container.clientWidth;
    const height = container.clientHeight;
    switch (region) {
        case "Popular on Social Media":
            return { x: width * 0.1, y: height * 0.6 }; // Lower center of the left side
        case "Large Market Value":
            return { x: width * 0.5, y: height * 0.1 };
        case "Easy to Buy/Sell":
            return { x: width * 0.9, y: height * 0.6 }; // Lower center of the right side
        case "Stable Price":
            return { x: width * 0.9, y: height * 0.9 };
        case "High Community Engagement":
            return { x: width * 0.1, y: height * 0.9 };
        default:
            return { x: width * 0.5, y: height * 0.5 };
    }
}

function getWeightedPosition(crypto) {
    const width = container.clientWidth;
    const height = container.clientHeight;
    const total = (crypto.mindshare / mindshareDivisor) + (crypto.marketCap / marketCapDivisor) + (crypto.liquidity / liquidityDivisor) + (crypto.price / priceDivisor) + (crypto.averageEngagementsCount / engagementsDivisor);
    const x = ((crypto.mindshare / mindshareDivisor) * 0.1 + (crypto.marketCap / marketCapDivisor) * 0.5 + (crypto.liquidity / liquidityDivisor) * 0.9 + (crypto.price / priceDivisor) * 0.9 + (crypto.averageEngagementsCount / engagementsDivisor) * 0.1) / total * width;
    const y = ((crypto.mindshare / mindshareDivisor) * 0.1 + (crypto.marketCap / marketCapDivisor) * 0.1 + (crypto.liquidity / liquidityDivisor) * 0.1 + (crypto.price / priceDivisor) * 0.9 + (crypto.averageEngagementsCount / engagementsDivisor) * 0.9) / total * height;
    return { x, y };
}

function updateCircles(cryptocurrencies) {
    const positions = [];

    for (const crypto of cryptocurrencies) {
        const region = getHighestValueRegion(crypto);
        if (!circles[crypto.agentName]) {
            circles[crypto.agentName] = new Circle(crypto, region);
        }
        const circle = circles[crypto.agentName];
        circle.region = region; // Update the region
        circle.element.style.backgroundColor = `rgb(${colors[region].r}, ${colors[region].g}, ${colors[region].b})`; // Update the color

        const weightedPosition = getWeightedPosition(crypto);
        let x = weightedPosition.x;
        let y = weightedPosition.y;

        for (const pos of positions) {
            const dx = x - pos.x;
            const dy = y - pos.y;
            const distance = Math.sqrt(dx * dx + dy * dy);
            if (distance < 100) {
                const angle = Math.atan2(dy, dx);
                x = pos.x + 100 * Math.cos(angle);
                y = pos.y + 100 * Math.sin(angle);
            }
        }

        positions.push({ x, y, color: colors[region] });

        circle.updatePosition(Math.max(0, Math.min(container.clientWidth - 100, x)), Math.max(0, Math.min(container.clientHeight - 100, y)));
    }
}

function getAverageCenter() {
    let totalX = 0, totalY = 0, count = 0;
    for (const sourceName in circles) {
        const source = circles[sourceName];
        totalX += source.element.offsetLeft + source.element.offsetWidth / 2;
        totalY += source.element.offsetTop + source.element.offsetHeight / 2;
        count++;
    }
    return { x: totalX / count, y: totalY / count };
}

function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    particles.forEach((particle, index) => {
        particle.update();
        if (particle.alpha <= 0) {
            particles.splice(index, 1);
        } else {
            particle.draw();
        }
    });

    const averageCenter = getAverageCenter();
    centralCircle.style.left = `${averageCenter.x - centralCircle.offsetWidth / 2}px`;
    centralCircle.style.top = `${averageCenter.y - centralCircle.offsetHeight / 2}px`;

    for (const sourceName in circles) {
        const source = circles[sourceName];
        const region = source.region;
        for (let i = 0; i < 3; i++) {
            particles.push(new Particle(averageCenter.x, averageCenter.y, source.element.offsetLeft, source.element.offsetTop, colors[region], colors[region]));
        }
    }
    requestAnimationFrame(animate);
}

async function fetchData() {
    const response = await fetch('/data');
    const data = await response.json();
    updateCircles(data);
    if (selectedCrypto) {
        const updatedCrypto = data.find(c => c.agentName === selectedCrypto.agentName);
        if (updatedCrypto) {
            selectedCrypto = updatedCrypto;
            updateDetails();
        }
    }
}

setInterval(fetchData, 5000);
animate();