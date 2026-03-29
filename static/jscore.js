document.addEventListener('DOMContentLoaded', () => {
    if (document.querySelector(".alert")) {
        setTimeout(() => {
            bootstrap.Alert.getOrCreateInstance(document.querySelector(".alert")).close();
        }, 5000);
    }

    if ((document.querySelector("#valor"))) {
        VMasker(document.querySelector("#valor")).maskMoney({
            precision: 2,
            separator: ',',
            delimiter: '.',
        });
    }

    document.querySelectorAll("[title='Deletar']").forEach((elem) => {
        elem.addEventListener("click", (e) => {
            if(!confirm("Tem certeza que deseja remover esta entrada?")) {
                e.preventDefault();
                return false;
            }
        });
    });
});




