let fetchInterval;

const homepage = document.querySelector(".home-page");
const execpage = document.querySelector(".exec-page");
const toExecPage = document.getElementById("mybtn1");
const toHomePage = document.getElementById("mybtn2");

const video = document.getElementById("video-feed");

function switchPage() {
    homepage.classList.toggle("active");
    execpage.classList.toggle("active");
}

toExecPage.addEventListener("click", () => {
    console.log("Try Now clicked");
    document.getElementById("video-feed").src = "http://localhost:5000/video_feed";
    
    fetchInterval = setInterval(() => {
        fetch('http://localhost:5000/coords')
            .then(res => {
                console.log("Fetch response:", res.status);
                return res.json();
            })
            .then(data => {
                console.log("Coords data:", data);
                document.getElementById("coords").innerText = `X: ${data.x}, Y: ${data.y}`;
            })
            .catch(error => console.error("Fetch error:", error));
    }, 100);

    switchPage();
});

toHomePage.addEventListener("click", () => {
    document.getElementById("video-feed").src = ""; 
    clearInterval(fetchInterval); 
    document.getElementById("coords").innerText = "X: 0, Y: 0";
    
    switchPage();
});