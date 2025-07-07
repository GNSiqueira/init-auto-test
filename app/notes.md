<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Carregamento Infinito</title>
    <style>
        
    </style>
</head>
<body>
    <div class="loading-container">
        <div class="loading-text">Carregando...</div>
        <div class="loading-spinner"></div>
        <div class="progress-bar">
            <div class="progress"></div>
        </div>
    </div>

    <script>
        // Simulação de carregamento infinito
        const loadingText = document.querySelector('.loading-text');
        const texts = ["Carregando dados...", "Processando informações...", "Aguarde um momento..."];
        let counter = 0;

        function changeText() {
            loadingText.textContent = texts[counter % texts.length];
            counter++;
            setTimeout(changeText, 2000);
        }

        changeText();

        // Animate dots for extra effect
        function animateDots() {
            let dots = '';
            for (let i = 0; i < counter % 4; i++) {
                dots += '.';
            }
            loadingText.textContent = texts[counter % texts.length] + dots;
            setTimeout(animateDots, 500);
        }

        animateDots();
    </script>
</body>
</html>
