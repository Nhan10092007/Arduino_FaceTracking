const homepage = document.querySelector(".home-page");
const execpage = document.querySelector(".exec-page");
const toExecPage = document.getElementById("mybtn1");
const toHomePage = document.getElementById("mybtn2");

toExecPage.addEventListener("click", switchPage);
toHomePage.addEventListener("click", switchPage);

function switchPage(){
    homepage.classList.toggle("active");
    execpage.classList.toggle("active");
}
