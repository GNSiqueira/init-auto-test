const loadingText = document.querySelector('.loading-text');
const texts = ["Carregando dados...", "Processando informações...", "Aguarde um momento..."];
let counter = 0;

function changeText() {
    loadingText.textContent = texts[counter % texts.length];
    counter++;
    setTimeout(changeText, 2000);
}
changeText();
function animateDots() {
    let dots = '';
    for (let i = 0; i < counter % 4; i++) {
        dots += '.';
    }
    loadingText.textContent = texts[counter % texts.length] + dots;
    setTimeout(animateDots, 500);
}
animateDots();