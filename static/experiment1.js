document.addEventListener("DOMContentLoaded", () => {
    const experimentName = "experiment1";
    const flipButton = document.getElementById("flip-button");
    const resetButton = document.getElementById("reset-button");
    const lastFlip = document.getElementById("last-flip");
    const totalFlips = document.getElementById("total-flips");
    const headsCount = document.getElementById("heads-count");
    const tailsCount = document.getElementById("tails-count");
    const headsProbability = document.getElementById("heads-probability");
    const tailsProbability = document.getElementById("tails-probability");
    const coin = document.getElementById("coin");

    let flipChart;
    const chartCanvas = document.getElementById("flipChart");
    const chartContext = chartCanvas.getContext("2d");

    function initChart() {
        if (flipChart) flipChart.destroy();

        flipChart = new Chart(chartContext, {
            type: "doughnut",
            data: {
                labels: ["Heads", "Tails"],
                datasets: [{
                    label: "Flip Results",
                    data: [0, 0],
                    backgroundColor: ["#3498db", "#e74c3c"],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: false,
                maintainAspectRatio: false,
                plugins: {
                    legend: { labels: { color: "#fff" } }
                }
            }
        });
    }

    async function fetchStats() {
        try {
            const response = await fetch(`/stats?experiment=${experimentName}`);
            const data = await response.json();

            totalFlips.textContent = data.total_flips;
            headsCount.textContent = data.heads_count;
            tailsCount.textContent = data.tails_count;
            headsProbability.textContent = `${Math.round(data.heads_probability)}%`;
            tailsProbability.textContent = `${Math.round(data.tails_probability)}%`;
            lastFlip.textContent = data.last_flip || "None";

            flipChart.data.datasets[0].data = [
                Math.max(0, data.heads_count || 0), 
                Math.max(0, data.tails_count || 0)
            ];
            flipChart.update();
        } catch (error) {
            console.error("Error fetching stats:", error);
        }
    }

    async function flipCoin() {
        try {
            const response = await fetch(`/flip?experiment=${experimentName}`);
            const data = await response.json();

            if (!data.flip_result) {
                console.error("Invalid response from server:", data);
                return;
            }

            let flipDuration = 0.6; 
            let rotations = Math.floor(Math.random() * 5) + 3;

            gsap.to(coin, { rotationY: 180 * rotations, duration: flipDuration, ease: "power2.inOut" });

            setTimeout(() => {
                if (data.flip_result === "Heads") {
                    console.log("Flipped: Heads");
                    coin.style.backgroundImage = "url('/static/front.png')";
                } else {
                    console.log("Flipped: Tails");
                    coin.style.backgroundImage = "url('/static/back.png')";
                }

                gsap.to(coin, { rotationY: 0, duration: 0.2 });
            }, flipDuration * 1000);

            fetchStats();
        } catch (error) {
            console.error("Error flipping coin:", error);
        }
    }

    async function resetExperiment() {
        try {
            await fetch(`/reset?experiment=${experimentName}`, { method: "POST" });

            totalFlips.textContent = "0";
            headsCount.textContent = "0";
            tailsCount.textContent = "0";
            headsProbability.textContent = "0%";
            tailsProbability.textContent = "0%";
            lastFlip.textContent = "None";

            flipChart.data.datasets[0].data = [0, 0];
            flipChart.update();

            fetchStats();
        } catch (error) {
            console.error("Error resetting experiment:", error);
        }
    }

    flipButton.addEventListener("click", flipCoin);
    resetButton.addEventListener("click", resetExperiment);

    initChart();
    fetchStats();
});
