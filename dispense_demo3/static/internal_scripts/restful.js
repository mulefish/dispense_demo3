function getPath() { 
    // let ip = document.getElementById("host").value 
    let address = "http://localhost:8080"
    return address
}
function yellowLog(msg) {
    console.log("%c " + msg , "background-color:yellow")
}
function greenLog(obj) {
    console.log("%c " + JSON.stringify(obj, null,2) , "background-color:yellow")
}

async function featured_products_curl() {
    try {
        const response = await fetch('http://localhost:8080/featured_products_curl', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({}) // Empty body
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        console.log('Response from featured_products_curl:', data);
    } catch (error) {
        console.error('Error posting to featured_products_curl:', error);
    }
}

async function checkHealth() {
    try {
        const response = await fetch('http://localhost:8080/healthcheck', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        console.log('Health Check Status:', data);
    } catch (error) {
        console.error('Error fetching health check:', error);
    }
}

// Call the function to check health
checkHealth();
