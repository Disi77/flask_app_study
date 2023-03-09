function calculatePrice() {
    var quantity = document.getElementById("quantity");
    var selectedProduct = document.getElementById("product");
    var subtotal = document.getElementById("subtotal");
    var calculation = document.getElementById("calculation");

    var products = document.getElementById("products");
    var productsList = JSON.parse(products.textContent)

    for(var i = 0, size = productsList.length; i < size; i++) {
        var item = productsList[i];
        var q = quantity.value;
        if (item["id"] == selectedProduct.value && q) {
            var price = item["price"];
            subtotal.innerHTML = price * q;
            calculation.innerHTML = `(${price} CZK * ${q} pcs)`;
            break;
        }
    }
};

var quantity = document.getElementById("quantity");
quantity.onchange = function () {
    calculatePrice();
};

var selectedProduct = document.getElementById("product");
selectedProduct.onchange = function () {
    calculatePrice();
};