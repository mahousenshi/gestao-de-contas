VMasker(document.querySelector("#valor")).maskMoney({
    precision: 2,
    separator: ',',
    delimiter: '.',
})

setTimeout(function() {
    bootstrap.Alert.getOrCreateInstance(document.querySelector(".alert")).close();
}, 5000)

