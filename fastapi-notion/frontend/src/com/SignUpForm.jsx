import React, { useState, useEffect } from 'react';
import styles from './styles_module.css';

function SignUpForm() {
  const [userData, setUserData] = useState({
    name: '',
    email: '',
    password: '',
    access_token: '',
    refresh_token: '',
    user_seq_no: ''
  });

  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    setUserData(prev => ({
      ...prev,
      access_token: urlParams.get('access_token') || '',
      refresh_token: urlParams.get('refresh_token') || '',
      user_seq_no: urlParams.get('user_seq_no') || ''
    }));
  }, []);

  const handleChange = (event) => {
    const { name, value } = event.target;
    setUserData(prevState => ({
      ...prevState,
      [name]: value
    }));
  };

  const handleAuth = () => {
    console.log("Redirecting to backend for authentication");
    window.location.href = "http://localhost:8000/login";
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    console.log("Submitting user info:", userData);

    try {
      const response = await fetch('http://localhost:8000/save_user_info', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(userData)
      });
      const data = await response.json();
      if (response.ok) {
        console.log("Response from server:", data);
        alert("User information saved successfully!");
      } else {
        console.error("Failed to save user info:", data);
        alert("Failed to save user information: " + JSON.stringify(data));
      }
    } catch (error) {
      console.error("Network or server error:", error);
      alert("Network or server error: " + error.message);
    }
  };

  return (
    <div className={styles.container}>
      <h2>SIGN UP</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Name</label>
          <input name="name" value={userData.name} onChange={handleChange} placeholder="Cristoval" />
        </div>
        <div>
          <label>Email</label>
          <input name="email" value={userData.email} onChange={handleChange} placeholder="abc@google.com" />
        </div>
        <div>
          <label>Password</label>
          <input name="password" value={userData.password} onChange={handleChange} placeholder="***" />
        </div>
        <div>
          <label>Access Token</label>
          <input name="access_token" value={userData.access_token} readOnly />
        </div>
        <div>
          <label>Refresh Token</label>
          <input name="refresh_token" value={userData.refresh_token} readOnly />
        </div>
        <div>
          <label>User Seq No</label>
          <input name="user_seq_no" value={userData.user_seq_no} readOnly />
        </div>
        <button type="button" onClick={handleAuth}>인증받기</button>
        <button type="submit">가입하기</button>
      </form>
    </div>
  );
}

export default SignUpForm;
