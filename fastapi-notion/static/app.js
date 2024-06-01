document.getElementById('authBtn').addEventListener('click', function() {
    console.log("Redirecting to backend for authentication");
    window.location.href = "http://localhost:8000/login";
});

window.onload = function() {
    const urlParams = new URLSearchParams(window.location.search);
    const access_token = urlParams.get('access_token');
    const refresh_token = urlParams.get('refresh_token');
    const user_seq_no = urlParams.get('user_seq_no');
    console.log("Page loaded with params:", { access_token, refresh_token, user_seq_no });
    if (access_token && refresh_token && user_seq_no) {
        document.getElementById('access_token').value = access_token;
        document.getElementById('refresh_token').value = refresh_token;
        document.getElementById('user_seq_no').value = user_seq_no;
    }
};

document.getElementById('signupBtn').addEventListener('click', function() {
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const access_token = document.getElementById('access_token').value;
    const refresh_token = document.getElementById('refresh_token').value;
    const user_seq_no = document.getElementById('user_seq_no').value;

    console.log("Submitting user info:", { name, email, password, access_token, refresh_token, user_seq_no });

    fetch('http://localhost:8000/save_user_info', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            name: name,
            email: email,
            password: password,
            access_token: access_token,
            refresh_token: refresh_token,
            user_seq_no: user_seq_no
        })
    }).then(response => response.json())
      .then(data => {
          console.log("Response from server:", data);
          alert(data.message);
      }).catch(error => {
          console.error("Error:", error);
      });
});
