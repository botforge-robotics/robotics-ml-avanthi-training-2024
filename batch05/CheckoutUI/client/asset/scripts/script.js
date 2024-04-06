var InitialCount = 0;

function getIpAddressFromUrl() {
    var currentUrl = window.location.href;
    var regex = /\/\/(.*?):/;
    var match = regex.exec(currentUrl);
    if (match && match.length > 1) {
        return match[1];
    } else {
        console.error('Failed to extract IP address from URL');
        return null;
    }
}

const ip = getIpAddressFromUrl();

const deleteProduct = async (productId) => {
    // Send a delete request to delete the product
    const url = `http://${ip}:3000/product/${productId}`;
    try {
        await axios.delete(url);
        // Reload the page after deletion
        location.reload();
    } catch (error) {
        console.error("Error deleting product:", error);
    }
}

const deleteProducts = async () => {
    url = `http://${ip}:3000/product`;

    let res = await axios.get(url);
    responseText = res.data;
    const products = responseText;
    console.log(products)
    for (let product of products) {
        const response = await axios.delete(`http://${ip}:3000/product/${product.id}`)
        console.log(response)
    }
    setTimeout(() => {
        location.reload();
        window.scroll({
            top: 0,
            left: 0,
            behavior: 'smooth'
        });
    }, 4000)

}

const loadProducts = async () => {
    url = `http://${ip}:3000/product`;

    let res = await axios.get(url);
    responseText = await res.data;
    const products = responseText;

    var len = 0
    var payable = 0;
    for (let product of products) {
        len += product.taken;
        payable = payable + parseFloat(product.payable);
    }

    if (len > InitialCount) {
        InitialCount = 0;
        blinkScreen()
        $("#1").css("display", "none");
        $("#home").css("display", "grid");
        $("#2").css("display", "grid");
        const products = responseText;
        console.log(products);
        document.getElementById('2').innerHTML = "CHECKOUT ₹" + payable;
        for (let product of products) {
            const existingProduct = document.getElementById(`product_${product.id}`);
            if (existingProduct) {
                // Update existing product's values
                existingProduct.querySelector('.card__unit span').textContent = `${product.taken}${product.unit}`;
                existingProduct.querySelector('.card__amount span').textContent = product.payable;
            } else {
                // Create new product element
                const x = `
                <section id="product_${product.id}">
                    <div class="card card-long animated fadeInUp once">
                        <img src="asset/img/${product.id}.jpg" class="album">
                        <div class="span1">Product Name</div>
                        <div class="card__product">
                            <span>${product.name}</span>
                        </div>
                        <div class="span2">Per Unit</div>
                        <div class="card__price">
                            <span>${product.price} </span>
                        </div>
                        <div class="span3">Units</div>
                        <div class="card__unit">
                            <span>${product.taken}${product.unit}</span>
                        </div>
                        <div class="span4">Payable</div>
                        <div class="card__amount">
                            <span>${product.payable}</span>
                        </div>
                        <button class="delete-button" onclick="deleteProduct('${product.id}')">Delete</button>
                    </div>
                </section>
            `;

                // Append new product to the home section
                document.getElementById('home').innerHTML += x;
            }

            InitialCount += product.taken;
        }
    }


}

var checkout = async () => {
    document.getElementById('2').innerHTML = "<span class='loader-16' style='margin-left: 44%;'></span>"
    var payable = 0;
    url = `http://${ip}:3000/product`;

    let res = await axios.get(url);
    responseText = await res.data;
    products = responseText;

    for (let product of products) {
        payable = payable + parseFloat(product.payable);
    }


    $("#home").css("display", "none");
    $("#final").css("display", "none");
    window.scroll({
        top: 0,
        left: 0,
        behavior: 'smooth'
    });
    var qrcode = new QRCode("qr", {
        text: `upi://pay?pa=8885221124@ybl&pn=8885221124&tn=cftrhwetaw4gta&am=${payable}`,
        width: 350,
        height: 370,
        colorDark: "#000000",
        colorLight: "#ecf0f3",
        correctLevel: QRCode.CorrectLevel.H
    });
    $("#qr").css("display", "grid");

    setTimeout(function () {
        $("#qr").css("display", "none");
        qrcode.clear();
        $("#success").css("display", "grid");
        deleteProducts();
    }, 10000);


}
function blinkScreen() {
    const body = document.body;
    body.style.opacity = '0.1'; // Lower opacity
    setTimeout(() => {
        body.style.opacity = '1'; // Full opacity after a delay
    }, 200); // Delay of 500 milliseconds
}