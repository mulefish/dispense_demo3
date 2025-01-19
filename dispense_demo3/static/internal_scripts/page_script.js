let latitude = undefined
let longitude = undefined

function toggleHamburger() {
    console.log("toggleHamburger() - this is a no-op")
}
function fa_rocket() {
    console.log("fa_rocket() - this is a no-op")
}

function fa_map() {
    console.log("fa_map() - this is a no-op")
}
//////////////////////////// 

function fa_user() {
    
    openuserModal() 
}


function openuserModal() {
    const userModal = document.getElementById("useruserModal");
    userModal.style.display = "block";
}

function closeuserModal() {
    const userModal = document.getElementById("useruserModal");
    userModal.style.display = "none";
}

// Close the userModal when the user clicks anywhere outside of it
window.onclick = function(event) {
    const userModal = document.getElementById("useruserModal");
    if (event.target === userModal) {
        closeuserModal();
    }
}

// Handle form submission
document.getElementById("userForm").onsubmit = function(event) {
    event.preventDefault();
    const firstName = document.getElementById("firstName").value;
    const lastName = document.getElementById("lastName").value;
    const email = document.getElementById("email").value;
    const phoneNumber = document.getElementById("phoneNumber").value;

    console.log("First Name:", firstName);
    console.log("Last Name:", lastName);
    console.log("Email:", email);
    console.log("Phone Number:", phoneNumber);


    closeuserModal();
};

//////////////////////////// 



// Get the current location
function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition, showError);
    } else {
        // document.getElementById('myLocation').innerHTML = "Geolocation is not supported by this browser.";
        console.log("%c Geolocation is not supported by this browser.", "background-color:yellow;")
    }
}




function showPosition(position) {
    function haversineDistance(lat1, lon1, lat2, lon2) {
        try {
            // Convert degrees to radians
            function toRadians(degrees) {
                return degrees * (Math.PI / 180);
            }

            // Radius of the Earth in miles
            const R = 3958.8;

            // Convert latitude and longitude from degrees to radians
            const φ1 = toRadians(lat1);
            const φ2 = toRadians(lat2);
            const Δφ = toRadians(lat2 - lat1);
            const Δλ = toRadians(lon2 - lon1);

            // Apply the Haversine formula
            const a = Math.sin(Δφ / 2) * Math.sin(Δφ / 2) +
                Math.cos(φ1) * Math.cos(φ2) *
                Math.sin(Δλ / 2) * Math.sin(Δλ / 2);
            const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));

            // Distance in miles
            const distance = R * c;
            return distance.toFixed(1);
        } catch (boom) {
            console.log("%c showPosition failure " + boom, "background-color:red;")
            return undefined
        }
    }


    latitude = position.coords.latitude
    longitude = position.coords.longitude

    // SET THE STORE DISTANCE! 
    for (let k in stores) {
        store = stores[k]
        const domId = "dist_" + store.name
        const miles = haversineDistance(store.lat, store.lon,latitude,longitude  )
        if ( miles !== undefined) {
            document.getElementById(domId).innerHTML = miles + " miles"
        }
    }


}

function showError(error) {
    console.log("showError")
    switch (error.code) {
        case error.PERMISSION_DENIED:
            document.getElementById('location').innerHTML = "User denied the request for Geolocation.";
            break;
        case error.POSITION_UNAVAILABLE:
            document.getElementById('location').innerHTML = "Location information is unavailable.";
            break;
        case error.TIMEOUT:
            document.getElementById('location').innerHTML = "The request to get user location timed out.";
            break;
        case error.UNKNOWN_ERROR:
            document.getElementById('location').innerHTML = "An unknown error occurred.";
            break;
    }
}

// Call getLocation on page load
window.onload = getLocation;