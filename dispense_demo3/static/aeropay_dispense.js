let bankToken = undefined;

function submit_to_get_aggregator_credentials() {
    console.log("%c submit_to_get_aggregator_credentials", "background-color:yellow")

    const t1 = new Date().getTime();

    fetch('/get_aggregator_credentials', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
    })
        .then(response => response.json())
        .then(data => {
            const milliseconds = new Date().getTime() - t1;
            document.getElementById("aggregator_receipt").value = "milliseconds: " + milliseconds + "\n" + JSON.stringify(data, null, 2);
            const aggregator_credentials_object = data;
            bankToken = data["token"];
            document.getElementById("bank_token").value = bankToken;

            // Initialize the Aerosync widget with the new bankToken
            initializeAerosyncWidget(bankToken);
        })
        .catch((error) => {
            const milliseconds = new Date().getTime() - t1;
            document.getElementById("aggregator_receipt").value = "milliseconds: " + milliseconds + "\n" + error;
        });
}

// Function to initialize the Aerosync widget
function initializeAerosyncWidget(token) {
    console.log("%c initializeAerosyncWidget", "background-color:yellow")

    var widgetRef = new window.AerosyncConnect({
        token: token, 
        id: "widget",
        iframeTitle: "Connect",
        width: "375px",
        height: "95%",
        environment: "staging", // "production",
        //   deeplink: deeplink,
        //   consumerId: consumerId,
        onEvent: function (type, payload) {
            console.log("onEvent", type, payload);
        },
        onLoad: function (event) {
            console.log("onLoad", event);
        },
        onSuccess: function (event) {
            var successData = document.getElementById("wrapData");
            successData.innerHTML = "";
            successData.innerText = "success : " + "\n" + JSON.stringify(event, null, 4);
            console.log("%c " + JSON.stringify(event, null, 2), "background-color:pink")
        },
        onBankAdded: function (event) {
        },
        onError: function (event) {
            console.log("onError", event);
            var errorData = document.getElementById("wrapData");
            errorData.innerHTML = "";
            errorData.innerText = "Error : " + "\n" + JSON.stringify(event, null, 4);
            console.log("%c OH NO" + JSON.stringify(event, null, 2), "background-color:pink")
        }
    });

    // launch the Aerosync widget on button click event.
    var openButton = document.getElementById('openBank');
    openButton.addEventListener('click', function () {
        widgetRef.launch();
    });
}
