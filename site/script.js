    // Event listeners para os botões de navegação
    document.getElementById('anterior').addEventListener('click', function () {
        if (paginaAtual > 1) {
            paginaAtual--;
            exibirDados();
        }
    });

    document.getElementById('proximo').addEventListener('click', function () {
        if (paginaAtual < totalPaginas) {
            paginaAtual++;
            exibirDados();
        }
    });