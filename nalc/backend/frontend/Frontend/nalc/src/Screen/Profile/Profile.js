import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import nalcLogo from '../../nalcLogo.png';
import './Profile.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import {faCheck, faTimes, faPen, faRightToBracket, faArrowLeft} from '@fortawesome/free-solid-svg-icons'

const UserProfile = () => {
  const [userProfile, setUserProfile] = useState({
    name: '',
    email: '',
    password: '',
  });
  const [editMode, setEditMode] = useState(false);
  const [tempProfile, setTempProfile] = useState({
    name: '',
    email: '',
    password: '',
  })
  const navigate = useNavigate();

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

  useEffect(() => {
    // Fetch user profile information
    fetchUserProfile();
  }, []); // Run once on component mount

  const fetchUserProfile = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/users/details/', {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('authToken')}`,
        },
      });
      setUserProfile(response.data); // Assuming response.data contains user information
    } catch (error) {
      console.error('Error fetching user profile:', error);
      // Handle error or redirect to login page
    }
  };

  const toggleEditMode = () => {
    setTempProfile(userProfile);
    setEditMode(!editMode);
  };

  const handleSaveChanges = async () => {
    try {
      // Perform API call to update user information
      const response = await axios.patch(
        'http://localhost:8000/api/users/update/',
        tempProfile, // Send updated user profile data
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('authToken')}`,
          },
        }
      );
      setUserProfile(response.data); // Assuming response.data contains updated user information
      setTempProfile({}); // Clear temporary profile after successful update
      toggleEditMode(); // Exit edit mode after successful update
    } catch (error) {
      console.error('Error updating user profile:', error);
      // Handle error
    }
  };

  const handleNameChange = (e) => {
    setTempProfile((prevTempProfile) => ({
      ...prevTempProfile,
      name: e.target.value,
    }));
  };
  
  const handleEmailChange = (e) => {
    setTempProfile((prevTempProfile) => ({
      ...prevTempProfile,
      email: e.target.value,
    }));
  };

  const handlePasswordChange = (e) => {
    setTempProfile((prevTempProfile) => ({
      ...prevTempProfile,
      password: e.target.value,
    }));
  };

  const goBack = () => {
    navigate('/home');
  }

  return (
    <div className='container-fluid-profile d-flex flex-column align-items-center justify-content-center'>
      <img
        src={nalcLogo}
        className="rounded mx-auto d-block logo-p mb-4"
        alt="NALC Logo"
        onClick={goBack}
      />
      <div className="card text-center" style={{ width: "30%" }}>
        <div className="head-color">
          <h2 className='textReg'><strong>User Profile</strong></h2>
        </div>
        <div className="card-body body-bg">
          <div className='row inputs'>
            {editMode ? (
              <form className="d-flex flex-column align-items-center">
                {/* Username */}
                <div className='inputFieldProf'>
                  <div className="label-wrapper">
                    <label className='text-maroonprof'><h3><strong>Username: </strong></h3></label>
                  </div>
                  <input
                    type='text'
                    name='name'
                    className="form-control"
                    id="floatingInput"
                    value={tempProfile.name || ''}
                    onChange={handleNameChange}
                    placeholder="Enter your username"
                  />
                </div>

                {/* Email */}
                <div className='inputFieldProf'>
                  <div className="label-wrapper">
                    <label className='text-maroonprof'><h3><strong>Email: </strong></h3></label>
                  </div>
                  <input
                    type='email'
                    name='email'
                    className="form-control"
                    id="floatingInput"
                    value={tempProfile.email || ''}
                    onChange={handleEmailChange}
                    placeholder="Enter your email"
                  />
                </div>

                {/* Password */}
                <div className='inputFieldProf'>
                  <div className="label-wrapper">
                    <label className='text-maroonprof'><h3><strong>Password: </strong></h3></label>
                  </div>
                  <input
                    type='password'
                    name='password'
                    className="form-control"
                    id="floatingInput"
                    value={tempProfile.password || ''}
                    onChange={handlePasswordChange}
                    placeholder="Enter your password"
                  />
                </div>

                {/* Save Changes and Cancel Buttons */}
                <div className="d-flex flex-row justify-content-center gap-2 mx-auto mt-3">
                  <button className='btn-registered' onClick={handleSaveChanges}>
                    <FontAwesomeIcon icon={faCheck} style={{ color: "#541212" }} />
                    &nbsp; Save
                  </button>
                  <button className='btn-registered' onClick={toggleEditMode}>
                    <FontAwesomeIcon icon={faTimes} style={{ color: "#541212" }} />
                    &nbsp; Cancel
                  </button>
                </div>
              </form>
            ) : (
              <div className="d-flex flex-column align-items-center">
                {/* Display Username */}
                <div className='inputFieldProf'>
                  <div className="label-wrapper">
                    <label className='text-maroonprof'><h3><strong>Username: </strong></h3></label>
                  </div>
                  <p className="form-control">{userProfile.name}</p>
                </div>

                {/* Display Email */}
                <div className='inputFieldProf'>
                  <div className="label-wrapper">
                    <label className='text-maroonprof'><h3><strong>Email: </strong></h3></label>
                  </div>
                  <p className="form-control">{userProfile.email}</p>
                </div>

                {/* Edit and Back Buttons */}
                <div className="d-flex flex-row justify-content-center gap-2 mx-auto mt-3">
                    <button className='btn-registered' onClick={toggleEditMode}>
                        <FontAwesomeIcon icon={faPen} style={{ color: "#541212" }} />
                        &nbsp; Edit
                    </button>
                    <button className='btn-registered' onClick={goBack}>
                        <FontAwesomeIcon icon={faArrowLeft} style={{ color: "#541212" }} />
                        &nbsp; Back
                    </button>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default UserProfile;