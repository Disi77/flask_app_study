function setValue(from, to) {
    var toElement = document.getElementById(to);
    var fromElement = document.getElementById(from);
    toElement.innerHTML = fromElement.value * 100;
};

var quantity = document.getElementById("quantity");
quantity.onchange = function () {
    setValue("quantity", "result");
};

window.onload = function () {
    setValue("quantity", "result");
};

