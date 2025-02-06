// Function to handle coin search
document.getElementById("search-bar").addEventListener("input", function () {
    let query = this.value.toLowerCase();
    let coinCards = document.querySelectorAll(".coin-card");
    
    coinCards.forEach(card => {
        let coinName = card.querySelector("h3").textContent.toLowerCase();
        if (coinName.includes(query)) {
            card.style.display = "block";
        } else {
            card.style.display = "none";
        }
    });
});

// Function to navigate to coin details page
function goToCoinDetails(coinId) {
    // Redirect to detailed page (could be a different file or a modal)
    window.location.href = `coin-details.html?id=${coinId}`;
}
