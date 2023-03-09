function setValue(from, to) {
    var fromElement = document.getElementById(from);
    var toElement = document.getElementById(to);
    toElement.innerHTML = fromElement.value * 100;
};

var quantity = document.getElementById("quantity");
quantity.onchange = function () {
    setValue("quantity", "result");
};

window.onload = function () {
    setValue("quantity", "result");
};

