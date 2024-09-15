import React, { useState } from 'react';
import axios from 'axios';
import './AdminScreen.css'
import nalcLogo from '../../nalcLogo.png';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import {faUpload, faRightFromBracket} from '@fortawesome/free-solid-svg-icons'

const AdminScreen = () => {
  const [file, setFile] = useState(null);

  // Set the initial token and headers
  axios.defaults.headers.common['Authorization'] = `Bearer ${localStorage.getItem('authToken')}`;

  // Set the session timeout duration (30 minutes in milliseconds)
  const sessionTimeoutDuration = 30 * 60 * 1000; // 30 minutes in milliseconds

  // Function to redirect the user to the login page
  const redirectToLogin = () => {
    window.location.href = '/';
  };

  // Function to reset the session timeout
  const resetSessionTimeout = () => {
    clearTimeout(sessionTimeout);
    sessionTimeout = setTimeout(redirectToLogin, sessionTimeoutDuration);
  };

  // Set the initial session timeout
  let sessionTimeout = setTimeout(redirectToLogin, sessionTimeoutDuration);

  // Attach an event listener to reset the session timeout on user activity
  document.addEventListener('mousemove', resetSessionTimeout);
  document.addEventListener('keydown', resetSessionTimeout);

  axios.interceptors.response.use(
    (response) => {
      resetSessionTimeout();
      return response;
    },
    (error) => {
      if (error.response && error.response.status === 401) {
        redirectToLogin();
      }
      return Promise.reject(error);
    }
  );

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    setFile(selectedFile);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('http://localhost:8000/upload-and-replace-data/', {
            method: 'POST',
            body: formData,
        });

        if (response.status === 200) {
            const data = await response.json(); // Parse JSON response
            if ('progress' in data) {
                console.log(`Progress: ${data.progress}%`);
            } else if ('message' in data) {
                alert(data.message); // Show success message
            }
        } else {
            const errorData = await response.json(); // Parse JSON error response
            alert(`Failed to add Data: ${errorData.error}`); // Show error message
        }
    } catch (error) {
        console.error("Error: ", error);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('authToken');
  
    redirectToLogin();
  };

  return (
    <div className='container-fluid-profile d-flex flex-column align-items-center justify-content-center'>
      <div className="top-left">
        <button className='replaceDataBtn' onClick={handleLogout}>
          <FontAwesomeIcon icon={faRightFromBracket} />
          &nbsp; Logout
        </button>
      </div>
      <div className='container-fluidity'>
      <div className="row d-block">
        <img
          src={nalcLogo}
          className="rounded mx-auto d-block logo-a mb-4"
          alt="NALC Logo"
          onClick={handleLogout}
        />
      </div>
      <div className='titleArea'>
        <h1 className='text-maroon'><strong>Admin Dashboard</strong></h1>
      </div>
      <form className='inputJson' onSubmit={handleSubmit}>
        <label htmlFor="fileInput" className="fileInputLabel">
          JSON File:
        </label>
        <input type="file"onChange={handleFileChange}/>
          <br />
          <button className='replaceDataBtn' type="submit">
            <FontAwesomeIcon icon={faUpload} />
            &nbsp; Submit
          </button>
      </form>
      </div>
    </div>
  );
};

export default AdminScreen;