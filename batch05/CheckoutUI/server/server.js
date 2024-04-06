const express = require('express')
const bodyParser = require('body-parser');
const cors = require('cors');

const app = express()
var port = process.env.PORT || 3000;

let products = [];
let orders = [];
app.use(cors());

app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

app.get('/', (req, res) => {
    res.send("API deployment successful");
});

app.post('/product', (req, res) => {
    // Extract product data from the request body
    const { id, name, price, unit, taken, payable } = req.body;
    console.log(req.body)
    // Check if a product with the same ID already exists
    const existingProductIndex = products.findIndex(product => parseInt(product.id) == parseInt(id));
    console.log(existingProductIndex)
    if (existingProductIndex !== -1) {
        // If the product exists, update 'taken' and 'payable' values
        products[existingProductIndex].taken += taken;
        products[existingProductIndex].payable += payable;
    } else {
        // Otherwise, add a new product to the database
        const product = {
            id: id,
            name: name,
            price: price,
            unit: unit,
            taken: taken,
            payable: payable
        };
        products.push(product);
    }
    console.log(products)
    // Send a response indicating success
    res.send('Product is added to the database');
});

app.get('/product', (req, res) => {
    // console.log(products)
    res.json(products);
});

app.get('/product/:id', (req, res) => {
    // reading id from the URL
    const id = req.params.id;

    // searching products for the id
    for (let product of products) {
        if (parseInt(product.id) == parseInt(id)) {
            res.json(product);
            return;
        }
    }

    // sending 404 when not found something is a good practice
    res.status(404).send('Product not found');
});

app.delete('/product/:id', (req, res) => {
    // reading id from the URL
    const id = req.params.id;

    // remove item from the products array
    products = products.filter(i => {
        if (parseInt(i.id) !== parseInt(id)) {
            console.log("not match")
            return true;
        }
        return false;
    });

    // sending 404 when not found something is a good practice
    res.send('Product is deleted');
});


app.listen(port, () => console.log(`Server listening on port ${port}!`));