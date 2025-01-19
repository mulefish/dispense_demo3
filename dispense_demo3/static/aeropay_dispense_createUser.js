function submit_to_create_user() {
    console.log("%c submit_to_create_user", "background-color:yellow")

    const t1 = new Date().getTime()
    const firstName = document.getElementById('first_name').value;
    const lastName = document.getElementById('last_name').value;
    const phoneNumber = document.getElementById('phone_number').value;
    const email = document.getElementById('email').value;
    let isOk = true
    if (firstName.length === 0) {
        document.getElementById("first_name_msg").innerHTML = "Need a first name"
        isOk = false
    } else {
        document.getElementById("first_name_msg").innerHTML = "first_name"
    }

    if (lastName.length === 0) {
        document.getElementById("last_name_msg").innerHTML = "Need a last name"
        isOk = false

    } else {
        document.getElementById("last_name_msg").innerHTML = "last_name"
    }

    var phoneRegex = /^\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})$/;
    if (!phoneRegex.test(phoneNumber)) {
        document.getElementById("phone_number_msg").innerHTML = "invalid phone format"
        isOk = false

    } else {
        document.getElementById("phone_number_msg").innerHTML = "phone_number"
    }

    var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
        document.getElementById("email_msg").innerHTML = "invalid email format"
        isOk = false

    } else {
        document.getElementById("email_msg").innerHTML = "email"
    }

    if (isOk === false) {
        return false
    }

    const data = {
        first_name: firstName,
        last_name: lastName,
        phone_number: phoneNumber,
        email: email
    };


    fetch('/send_user_data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
        .then(response => response.json())
        .then(data => {
            const milliseconds = new Date().getTime() - t1
            document.getElementById("create_user_receipt").value = "milliseconds: " + milliseconds + "\n\n" + JSON.stringify(data, null, 2)
            const user_object = data
            const bearerToken = data["bearer_token_was"]
            document.getElementById("bearer_token").value = bearerToken

        })
        .catch((error) => {
            const milliseconds = new Date().getTime() - t1
            document.getElementById("create_user_receipt").value = "milliseconds: " + milliseconds + "\n\n" + error
        });
}
