// globals
let inventory;
let stores;
let featuredProducts;
let storeMap;
const searchInputField = document.getElementById("searchInputField");
// end globals
const GET_STORES="get_stores"
const GET_INVENTORY = "get_inventory"
async function load_data_from_db(cmd) { 
    if ( cmd == GET_STORES) {
        try {
            const response = await fetch(GET_STORES);
            if (!response.ok) {
                throw new Error('Network response was not ok' + response.statusText);
            }
            const result = await response.json();
            return result;
        } catch (error) {
            console.error('There has been a problem with fetching ' + pathToBallOfJson, error);
        }
    }
    else if ( cmd == GET_INVENTORY ) {
        const response = await fetch(GET_INVENTORY);
        if (!response.ok) {
            throw new Error('Network response was not ok' + response.statusText);
        }
        const result = await response.json();
        return result;
    
    } else {
        alert("cmd " + cmd + " not found!")
    }
}

async function loadJSON(pathToBallOfJson) {
    try {
        const response = await fetch(pathToBallOfJson);
        if (!response.ok) {
            throw new Error('Network response was not ok' + response.statusText);
        }
        const result = await response.json();
        return result;
    } catch (error) {
        console.error('There has been a problem with fetching ' + pathToBallOfJson, error);
    }
}

function resetSearchChoices() {
    const cbd = document.getElementById('cbd')
    const thc = document.getElementById('thc')
    const productStyle = document.getElementById('productStyle')
    cbd.selectedIndex = 0
    thc.selectedIndex = 0
    productStyle.selectedIndex = 0
}
function getSearchChoices() {

    const cbd = document.getElementById('cbd');
    const cbdValue = cbd.value;

    const thc = document.getElementById('thc');
    const thcValue = thc.value;

    const productStyle = document.getElementById('productStyle');
    const productStyleValue = productStyle.value;

    const limiter = {
        cbd: parseInt(cbdValue), // 0 means anything is ok 
        thc: parseInt(thcValue), // 0 means anything is ok
        productStyle: productStyleValue
    }
    return limiter
}
function getStoreNameFromStoreId(storeId) {
    let storeName = "unknown"
    for (let k in storeMap) {
        if (storeMap[k].storeId == storeId) {
            storeName = storeMap[k].name
        }
    }
    return storeName
}

function setBackgroundOfItemsInTheCart() {
    const cart = JSON.parse(localStorage.getItem('cart')) || [];
    for (let k in cart) {
        const element = document.getElementById(cart[k].productUUID);
        if (element) {
            element.style.backgroundColor = "yellow";
        }
    }
}


async function populateStoreTiles() {
    // stores = await loadJSON('datastore/store.json');
    stores = await load_data_from_db(GET_STORES);
    storeMap = {}
    for (let i = 0; i < stores.length; i++) {
        storeMap[stores[i].storeId] = stores[i]
    }
    let row = `<table border='1' id="stores"><tr>`;
    for (let i = 0; i < stores.length; i++) {
        const store = stores[i];
        row += `<td onmouseenter="handleMouseEnterStoreTile(this)" 
                    onmouseleave="handleMouseLeaveStoreTile(this)"
                    onclick="handleStoreTileClick('${store.storeId}')"
        ><div class="container" >
        <img class="product-image" src="/static/images/${store.image}" alt="${store.image}">
        <div class="product-tile">
            <div class="product-info">
                <h2>${store.name}</h2>
                <h5>
                Address:${store.address}
                <strong>Phone:</strong> ${store.phone}
                <div id="dist_${store.name}"></div> <!-- dynamically set when/if location is known -->
                </h5>
                <button onclick="event.stopPropagation(); openStoreMapModal('${store.storeId}')">Map</button>
                <button onclick="event.stopPropagation(); viewInventoryForStore('${store.storeId}')">Menu</button>
            </div>
        </div></td>`;
    }
    row += "</tr></table>";
    document.getElementById("viewport").innerHTML = row;
}
function handleMouseEnterStoreTile(storeTile) {
    storeTile.style.backgroundColor = '#f0f0f0'
}

function handleMouseLeaveStoreTile(storeTile) {
    storeTile.style.backgroundColor = '';
}



function isOkToUseThisItem(cbd, thc, productStyle, candidateEntry) {
    let keep = true
    if (cbd > 0) {
        keep &&= candidateEntry.hasOwnProperty("cbd") && candidateEntry["cbd"] >= cbd
    }
    if (thc > 0) {
        keep &&= candidateEntry.hasOwnProperty("thc-a") && candidateEntry["thc-a"] >= thc
    }

    if (productStyle !== "any") {
        keep &&= candidateEntry.hasOwnProperty("type") && candidateEntry["type"].toLowerCase() === productStyle
    }
    // console.log(keep, cbd, thc, productStyle)
    return keep
}

async function viewInventoryForStore(storeId) {
    if (inventory === undefined) {
        // inventory = await loadJSON("datastore/inventory.json");
        inventory = await load_data_from_db(GET_INVENTORY)
    }
    
    const a = sillyMusicalNotes_thisFuncReallyDoesNotNeedToExist_IthoughtItCute()
    const b = sillyMusicalNotes_thisFuncReallyDoesNotNeedToExist_IthoughtItCute()

    const storeName = getStoreNameFromStoreId(storeId)


    console.log("%c viewInventoryForStore storeId is " + storeId  + " and " + storeName + " len "+ inventory.length  , "background-color:lightgreen;")


    let row = `<h1>${a} ${storeName} ${b}</h1><table border='1'><tr>`;

    let count = 0;

    const limitingChoices = getSearchChoices()
    const cbd = limitingChoices["cbd"]
    const thc = limitingChoices["thc"]
    const productStyle = limitingChoices["productStyle"]

    for (let i = 0; i < inventory.length; i++) {
        if (inventory[i].storeId_fk == storeId) {

           const obj = inventory[i] 
           const detail_obj = obj["JSON"];

            const keep = isOkToUseThisItem(cbd, thc, productStyle, detail_obj)

            if (keep === true) {

                let details = "";
                for (let k in detail_obj) {
                    details += `<strong>${k}:</strong>${detail_obj[k]}<br/>`;
                }

                details += `<strong>instock:</strong>${obj['instock']}<br/>`;
                details += `<strong>price:</strong>${obj['price']}<br/>`;
                details += `<strong>uid:</strong>${obj['uid']}<br/>`;


                //  console.log(  obj.uid )
                row += `<td valign='top'>
                <div class="container">
                    <div class="product-tile" id='${obj.uid}'>
                        <img src="images/inventory/${obj.img}" width="130" ></img>
                        <div class="product-info">
                            ${details}

                        <button onclick="addToCart('${obj.uid}', '${obj.price}')">Add to cart</button>
                        <button onclick="cartBtnClick()">Cart View</button>
                        </div>
                    </div>
                </div>
            </td>`;
                count++;
                // Add a new row every 5th item
                if (count % 6 === 0 && count !== 0) {
                    row += "</tr><tr>";
                }
            }
        }
    }
    row += "</table>";
    document.getElementById("showing").innerHTML = row;
    setBackgroundOfItemsInTheCart()

}

//// ////////////// CART ////////////////// 
function addToCart(productUUID, price) {

    let cart = JSON.parse(localStorage.getItem('cart')) || [];
    const existingProductIndex = cart.findIndex(item => item.productUUID === productUUID);
    if (existingProductIndex !== -1) {
        cart[existingProductIndex].quantity += 1;
    } else {
        cart.push({ productUUID: productUUID, quantity: 1, price: price });
    }

    // Save the updated cart back to localStorage
    localStorage.setItem('cart', JSON.stringify(cart));

    // Update the cart UI and cart count
    updateCartUI();
    updateCartCount();

    ///    console.log( JSON.stringify( cart, null,2  )) 

}

// Function to update the cart UI (optional)
function updateCartUI() {
    const cart = JSON.parse(localStorage.getItem('cart')) || [];
    for (let k in cart) {
        const element = document.getElementById(cart[k].productUUID);
        if (element) {
            element.style.backgroundColor = "yellow";
        }
        // document.getElementById(cart[k].productUUID).style.backgroundColor=yellow;
    }
    const cartContainer = document.getElementById('cart-container');
    let html = "<table border='1'>";
    html += "<tr><th></th><th>UUID</th><th>Quantity</th><th>Price</th></tr>";
    cart.forEach(item => {
        const removeBtn = `<button onclick="removeItem('${item.productUUID}')">Remove</button>`;
        html += "<tr>";
        html += `<td>${removeBtn}</td>`;
        html += `<td>${item.productUUID}</td>`;
        html += `<td>${item.quantity}</td>`;
        html += `<td>${item.price}</td>`;
        html += "</tr>";
    });
    html += "</table>";
    cartContainer.innerHTML = html;
}

// Function to update the cart count
function updateCartCount() {
    const cart = JSON.parse(localStorage.getItem('cart')) || [];
    const cartCount = cart.reduce((total, item) => total + item.quantity, 0);
    document.getElementById('cart_count').textContent = cartCount;
}

// Function to remove an item from the cart
function removeItem(productUUID) {
    const element = document.getElementById(productUUID);
    if (element) {
        element.style.backgroundColor = "";
    }

    let cart = JSON.parse(localStorage.getItem('cart')) || [];
    cart = cart.filter(item => item.productUUID !== productUUID);

    // Save the updated cart back to localStorage
    localStorage.setItem('cart', JSON.stringify(cart));

    // Update the cart UI and cart count
    updateCartUI();
    updateCartCount();
}

// Call this function on page load to initialize the cart UI and cart count
document.addEventListener('DOMContentLoaded', () => {
    updateCartUI();
    updateCartCount();
});

// Modal functionality
const cartModal = document.getElementById("cartModal");
// const cartBtn = document.getElementById("cartButton");
const cartClose = document.getElementById("closeCartModal");

function cartBtnClick() {
    updateCartUI(); // Ensure the cart UI is updated when opening the modal
    cartModal.style.display = "block";
}

cartClose.onclick = function () {
    cartModal.style.display = "none";
}

window.onclick = function (event) {
    if (event.target == cartModal) {
        cartModal.style.display = "none";
    }
}


function sillyMusicalNotes_thisFuncReallyDoesNotNeedToExist_IthoughtItCute() {
    // List of Font Awesome musical note and instrument icons
    const notes = [
        '<i class="fas fa-music green-icon"></i>',        // Music note
        '<i class="fas fa-guitar green-icon"></i>',       // Guitar
        '<i class="fas fa-drum green-icon"></i>',         // Drum
        '<i class="fas fa-headphones green-icon"></i>',   // Headphones
        '<i class="fas fa-microphone green-icon"></i>',   // Microphone
        '<i class="fas fa-saxophone green-icon"></i>',    // Saxophone
        '<i class="fas fa-trumpet green-icon"></i>',      // Trumpet
        '<i class="fas fa-piano green-icon"></i>',        // Piano
        '<i class="fas fa-violin green-icon"></i>',       // Violin
        '<i class="fas fa-stethoscope green-icon"></i>',  // Medical stethoscope
        '<i class="fas fa-hospital green-icon"></i>',     // Hospital
        '<i class="fas fa-first-aid green-icon"></i>',    // First aid kit
        '<i class="fas fa-notes-medical green-icon"></i>',// Medical notes
        '<i class="fas fa-cannabis green-icon"></i>',     // Marijuana leaf
        '<i class="fas fa-joint green-icon"></i>',        // Joint
        '<i class="fas fa-prescription-bottle green-icon"></i>', // Prescription bottle
        '<i class="fas fa-clinic-medical green-icon"></i>',// Medical clinic
        '<i class="fas fa-vial green-icon"></i>',         // Medical vial
        '<i class="fas fa-vials green-icon"></i>',        // Multiple vials
        '<i class="fas fa-capsules green-icon"></i>',     // Capsules
        '<i class="fas fa-prescription green-icon"></i>', // Prescription icon
        '<i class="fas fa-vending-machine green-icon"></i>', // Vending machine
        '<i class="fas fa-heartbeat green-icon"></i>'     // Heartbeat (medical)
    ];
    // Randomly determine the number of notes (between 2 and 6)
    const numNotes = Math.floor(Math.random() * 5) + 2;

    // Shuffle and select random notes
    const selectedNotes = [];
    for (let i = 0; i < numNotes; i++) {
        const randomIndex = Math.floor(Math.random() * notes.length);
        selectedNotes.push(notes[randomIndex]);
    }

    // Return the joined string of selected notes
    return selectedNotes.join(' ');

}
async function handleStoreTileClick(storeIdAsString) {
    console.log("%c handleStoreTileClick", "background-color:lightgreen;")

    const storeId = parseInt(storeIdAsString)
    if (featuredProducts === undefined) {
        featuredProducts = await loadJSON("datastore/store_inventory_featuredProducts.json");
    }

    const a = sillyMusicalNotes_thisFuncReallyDoesNotNeedToExist_IthoughtItCute()
    const b = sillyMusicalNotes_thisFuncReallyDoesNotNeedToExist_IthoughtItCute()

    const storeName = getStoreNameFromStoreId(storeId)

    let row = `<h1>${a} FEATURED PRODUCTS for ${storeName} ${b}</h1><table border='1'><tr>`;
    let count = 0
    featuredProducts.forEach((obj) => {
        if (obj.storeId_fk === storeId) {
            let detail_obj = JSON.parse(obj.JSON);
            let details = `<h2>${obj.description}</h2>`;
            for (let k in detail_obj) {
                details += `<strong>${k}:</strong>${detail_obj[k]}<br/>`;
            }

            details += `<strong>instock:</strong>${obj['instock']}<br/>`;
            details += `<strong>price:</strong>${obj['price']}<br/>`;
            details += `<strong>uid:</strong>${obj['uid']}<br/>`;

            //  console.log(  obj.uid )
            row += `<td>
                <div class="container">
                    <div class="product-tile" id='${obj.uid}'>
                        <img src="images/inventory/${obj.img}" width="130" ></img>
                        <div class="product-info">
                            ${details}
                        <button onclick="addToCart('${obj.uid}', '${obj.price}')">Add to cart</button>
                        <button onclick="cartBtnClick()">Cart View</button>
                        </div>
                    </div>
                </div>
            </td>`;

            count++;

            // Add a new row every 5th item
            if (count % 6 === 0 && count !== 0) {
                row += "</tr><tr>";
            }
        }
    })
    row += "</table>";
    document.getElementById("showing").innerHTML = row;

    setBackgroundOfItemsInTheCart()

}

function metaDescriptors(candidateToken) {
    candidateToken = candidateToken.toLowerCase()
    let whatIsItGoodFor = {
        "anxiety": "sativa",
        "elevates": "sativa",
        "energy": "sativa",
        "energizing": "sativa",
        "appetite": "sativa",
        "fatigue": "sativa",
        "happy": "sativa",
        "memory": "sativa",
        "relax": "indica",
        "pain": "indica",
        "calm": "indica",
        "dream": "indica",
        "upset": "indica",
        "help": "indica",
    }
    if (whatIsItGoodFor.hasOwnProperty(candidateToken)) {
        return whatIsItGoodFor[candidateToken]
    }
}
async function search() {


    if (inventory === undefined) {
        inventory = await loadJSON("datastore/inventory.json");
    }

    const limitingChoices = getSearchChoices()
    const cbd = limitingChoices["cbd"]
    const thc = limitingChoices["thc"]
    const productStyle = limitingChoices["productStyle"]


    const seek = searchInputField.value.toLowerCase();
    if (seek == null || seek.length < 3) {
        alert("Silly! You need to search for something to search: At least 3 chars long.");
        return;
    }
    const soughtFor = seek.split(/[^a-z0-9]+/).filter(word => word.length > 0);
    for (let i = 0; i < soughtFor.length; i++) {
        const maybe = metaDescriptors(soughtFor[i])
        if (maybe != undefined) {
            soughtFor.push(maybe)
        }
    }


    let found = {};
    for (let i = 0; i < inventory.length; i++) {

        const detail_obj = JSON.parse(inventory[i].JSON);
        const keep = isOkToUseThisItem(cbd, thc, productStyle, detail_obj)
        if (keep === true) {
            //console.log("%c yay search keep " + keep , "background-color:lightgreen;")

            for (let j = 0; j < soughtFor.length; j++) {
                if (inventory[i].JSON.toLowerCase().indexOf(soughtFor[j]) > -1) {
                    if (found.hasOwnProperty(i)) {
                        found[i]['seen']++;
                    } else {
                        found[i] = {
                            seen:1,
                            token:soughtFor[j]
                        }
                    }
                }
            }
        } else {
            //console.log("%c boo search keep " + keep , "background-color:lightgreen;")

        }
    }
    let ary = []
    for (k in found) {
        ary.push({ index: k, seen: found[k]['seen'], token:found[k]['token'] })
    }
    ary.sort((a, b) => b.seen - a.seen);
    const a = sillyMusicalNotes_thisFuncReallyDoesNotNeedToExist_IthoughtItCute()
    const b = sillyMusicalNotes_thisFuncReallyDoesNotNeedToExist_IthoughtItCute()

    let row = `<h1>${a} ${soughtFor} ${b}</h1><table border='0'><tr>`;
    let count = 0

    if (ary.length > 0) {
        for (let i = 0; i < ary.length; i++) {
            const lookup = ary[i]
            const obj = inventory[lookup.index]

            const storeId_fk = inventory[lookup.index].storeId_fk
            const store = storeMap[storeId_fk]
            let detail_obj = JSON.parse(obj.JSON);
            let details = `<h2>${store.name}</h2>`;
            for (let k in detail_obj) {
                details += `<strong>${k}:</strong>${detail_obj[k]}<br/>`;
            }

            details += `<strong>instock:</strong>${obj['instock']}<br/>`;
            details += `<strong>price:</strong>${obj['price']}<br/>`;
            details += `<strong>uid:</strong>${obj['uid']}<br/>`;
            row += `<td valign='top'>
            <div class="container">
                <div class="product-tile" id='${obj.uid}'>
                    <img src="images/inventory/${obj.img}" width="130" ></img>
                    <div class="product-info">
                        ${details}
                    <button onclick="addToCart('${obj.uid}', '${obj.price}')">Add to cart</button>
                    <button onclick="cartBtnClick()">Cart View</button>
                    </div>
                </div>
            </div>
        </td>`;
            count++;
            if (count % 6 === 0 && count !== 0) {
                row += "</tr><tr>";
            }
        }
    }
    else {
        row += `<tr><td><i class="fas fa-sad-tear sad_icon"></i></td></tr>`
        row += `<tr><td><div class="sad_msg">Nothing was found.</div></td></tr>`
    }
    row += "</table>";
    document.getElementById("showing").innerHTML = row;


    setBackgroundOfItemsInTheCart()

    // DEBUG! Working on weighted search!
    const currentUrl = window.location.href;
    const isDebugModeUrl = new URL(currentUrl);
    const params = new URLSearchParams(isDebugModeUrl.search);
    if (params.has("debug")) {
        console.log("%c DEBUG SEARCH!", "background-color:yellow;");
        console.log(JSON.stringify(ary, null, 2))
    }
}




