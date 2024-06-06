import React, { useState } from 'react';
import styles from './styles_module.css';

function UserInfo() {
  const [userInfo, setUserInfo] = useState(null);
  const [accessToken, setAccessToken] = useState('');
  const [userSeqNo, setUserSeqNo] = useState('');

  const handleGetUserInfo = async () => {
    try {
      const response = await fetch(`http://localhost:8000/get_user_info?access_token=${accessToken}&user_seq_no=${userSeqNo}`, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
      });
      const data = await response.json();
      if (response.ok) {
        setUserInfo(data);
      } else {
        console.error("Failed to get user info:", data);
        alert("Failed to get user information: " + data.error);
      }
    } catch (error) {
      console.error("Network or server error:", error);
      alert("Network or server error: " + error.message);
    }
  };

  return (
    <div className={styles.container}>
      <h2>USER INFO</h2>
      <div>
        <label>Access Token</label>
        <input name="accessToken" value={accessToken} onChange={(e) => setAccessToken(e.target.value)} placeholder="Enter Access Token" />
      </div>
      <div>
        <label>User Seq No</label>
        <input name="userSeqNo" value={userSeqNo} onChange={(e) => setUserSeqNo(e.target.value)} placeholder="Enter User Seq No" />
      </div>
      <button onClick={handleGetUserInfo}>Get User Info</button>
      {userInfo && (
        <div>
          <h3>User Information</h3>
          <pre>{JSON.stringify(userInfo, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default UserInfo;
