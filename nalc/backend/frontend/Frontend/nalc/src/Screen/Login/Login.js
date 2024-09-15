import React , {useState} from 'react';
import axios from 'axios';
import {useNavigate} from 'react-router-dom';
import { lineWobble } from 'ldrs';
import nalcLogo from '../../nalcLogo.png';
import './Login.css';

function Login() {
  lineWobble.register();
  const [email , setEmail] = useState("");
  const [pwd , setPwd] = useState("");
  const navigate = useNavigate();
  const [forgetPwdEmail, setForgetPwdEmail] = useState("");
  const [loginLoading , setLoginLoading] = useState(false);

  const handleLogin = async () => {
    try {
      setLoginLoading(true);
      const response = await axios.post('http://localhost:8000/api/users/login/', {
        email: email,
        password: pwd,
      });
      if (response.status >= 200 && response.status < 300) {
        // Save auth token
        const authToken = response.data.access_token;

        // Add the token to the headers for subsequent requests
        localStorage.setItem('authToken', authToken);

        // Check if the user is a superuser
        if (response.data.is_superuser) {
          navigate('/admin'); // Redirect to the admin page if the user is a superuser
        } else {
          navigate('/home'); // Redirect to the home page for regular users
        }
      } else {
        alert('Email or Password is incorrect');
      }
    } catch (error) {
      console.error('Login failed:', error);
      alert("Email or Password is incorrect");
    } finally{
      setLoginLoading(false);
    }
  };

  const handleRegister = () => {
    window.location.href = '/register';
  }

  const handleEmailChange = (event) => {
    setEmail(event.target.value);
  };

  const handlePwdChange = (event) => {
    setPwd(event.target.value);
  };

  const handleForgetPwdEmail = (event) => {
    setForgetPwdEmail(event.target.value);
  };

  const handleForgetPwd = async () => {
    try {
      const response = await axios.post('https://nalc-backend-ebe218d27802.herokuapp.com/api/reset-password/', {
        email: forgetPwdEmail,
      });
    
      const responseBody = response.data;
    
      // Check if the email field in the response is empty
      if (responseBody.email && responseBody.email[0] === "") {
        alert("Email field is empty. Please provide a valid email.");
      } else {
        // Display a custom success message
        alert("Password reset request submitted successfully!");
      }
    } catch (error) {
      console.error(error);
    
      // Handle error response (if applicable)
      if (error.response) {
        const errorResponseBody = error.response.data;
    
        // Check if the email field in the error response is empty
        if (errorResponseBody.email && errorResponseBody.email[0] === "") {
          alert("Email field is empty in the error response. Please provide a valid email.");
        } else {
          // Display a custom error message
          alert("An error occurred while processing your request. Please try again.");
        }
      } else {
        // Handle other types of errors (e.g., network errors)
        alert('An error occurred. Please try again.');
      }
    }
  };
  
  return (
    <>
      {/* Modal */}
        <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
          <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
              <div class="modal-header">
                <h1 class="modal-title fs-5" id="exampleModalLabel">Forget password</h1>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
              </div>
              <div class="modal-body">
                  <label htmlFor="floatingInputValue">Enter Email:</label>
                  <input type="email" className="form-control" id="floatingInputValue" onChange={handleForgetPwdEmail} placeholder="name@example.com" />
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                <button type="button" class="btn btn-primary" onClick={handleForgetPwd}>Submit</button>
              </div>
            </div>
          </div>
        </div>
      <div className="container-fluid gx-0">
        <div className="title" style={{ backgroundColor: '#FFF4C5' }}>
          <div className="row logo">
            <img src={nalcLogo} alt="NALC Logo" />
          </div>
          <div className="row words">
            <h1>
              <strong>
                  Narrative Association for Linked Content
                  for IPAMS
              </strong>
              <br />
              <small style={{ fontSize: '60%' }}>
                (Intellectual Property Asset Management System)
              </small>
            </h1>
          </div>
        </div>
        <div className="form">
          <div className='row'>
            <h1 style={{color: '#841818' }}>Login Account</h1>
          </div>
          <br/>
          <div className='row inputs'>
            <form>
                <div className='inputField' style={{width: 370, height: 48, position: 'relative'}}>
                    <input type="email" class="form-control" id="floatingInput" placeholder="Email" onChange={handleEmailChange} 
                      onKeyDown={(e) => {
                        if (e.key === "Enter") {
                          e.preventDefault();
                          handleLogin();
                        }}}
                      />
                    <div style={{width: 6, height: 35, left: 0, top: 0, position: 'absolute', background: '#841818'}} />
                </div>
                <div className='inputField' style={{width: 370, height: 48, position: 'relative'}}>
                    <input type="password" class="form-control" id="floatingInput" placeholder="Password" onChange={handlePwdChange}
                      onKeyDown={(e) => {
                        if (e.key === "Enter") {
                          e.preventDefault();
                          handleLogin();
                        }}}
                    />
                    <div style={{width: 6, height: 35, left: 0, top: 0, position: 'absolute', background: '#841818'}} />
                </div>
                <div class="l-grid gap-2">
                  <button className="createAcc text-maroon" onClick={handleRegister} type="button"><strong> Register Now! </strong></button>
                  <br/>
                </div>
                <button class="btn-login" type="button" onClick={handleLogin}>Login</button>
            </form>
          </div>
          <br/>
            {loginLoading && 
            <div className='row'>
              <l-line-wobble
                size="80"
                stroke="5"
                bg-opacity="0"
                speed="2"
                color="#841818" 
              ></l-line-wobble>
            </div>
            }
        </div>
      </div>
    </>
  );
}

export default Login;
