import React, { useState } from 'react';
import axios from 'axios';
import {useNavigate} from 'react-router-dom';
import { lineWobble } from 'ldrs';
import nalcLogo from '../../nalcLogo.png';
import './Register.css';
import { faL } from '@fortawesome/free-solid-svg-icons';

function Register() {
  lineWobble.register();

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const navigate = useNavigate();
  const [regLoading , setRegLoading] = useState(false);

  const handleRegister = async () => {
    try {
      setRegLoading(true);
      const response = await axios.post('http://localhost:8000/api/users/register/', {
        email: email,
        password: password,
        name: name,
      });
  
      if (response.status === 201) {
        // Registration Successful
        navigate('/');
      }
    } catch (error) {
      // Registration failed
      if (error.response && error.response.status === 400) {
        // Bad Request - Email validation error
        alert('Please provide a valid email address.');
  
        // Additional: Log the details of the validation error to the console
        if (error.response.data && error.response.data.details) {
          // No console.log here
        }
      } else if (error.response && error.response.status === 409) {
        // Conflict - Email already in use
        alert('This email is already in use. Please use a different email.');
      } else {
        // Other errors
        alert('An error occurred during registration. Please try again.');
      }
    } finally{
      setRegLoading(false);
    }
  };

  const handleLogin = () =>{
    window.location.href = '/';
  }
  

  const handleInputChange = (identifier) => (e) =>{
    if(identifier == 'email'){
      setEmail(e.target.value);
    } else if (identifier == 'name'){
      setName(e.target.value);
    } else if (identifier == 'pwd'){
      setPassword(e.target.value);
    }
  }
  return (
    <div className='containter-fluid'>
      <img src={nalcLogo} className="rounded mx-auto d-block logo-r" alt="NALC Logo"></img>
      <div class="card text-center" style={{ width: "50%" , margin: "auto" }}>
        <div class=" head-color">
          <h2 className='textReg'><strong>Create Account</strong></h2>
        </div>
        <div class="card-body body-bg">
          <br/>
          <div className='row inputs'>
            <form>
                <div className='inputField' style={{width: 370, height: 48, position: 'relative'}}>
                    <input type="email" class="form-control" id="floatingInput" placeholder="Email" required onChange={handleInputChange('email')}/>
                    <div style={{width: 6, height: 35, left: 0, top: 0, position: 'absolute', background: '#841818'}} />
                </div>
                <div className='inputField' style={{width: 370, height: 48, position: 'relative'}}>
                    <input type="text" class="form-control" id="floatingInput" placeholder="Name" required onChange={handleInputChange('name')}/>
                    <div style={{width: 6, height: 35, left: 0, top: 0, position: 'absolute', background: '#841818'}} />
                </div>
                <div className='inputField' style={{width: 370, height: 48, position: 'relative'}}>
                    <input type="password" class="form-control" id="floatingInput" placeholder="Enter Password" required onChange={handleInputChange('pwd')}/>
                    <div style={{width: 6, height: 35, left: 0, top: 0, position: 'absolute', background: '#841818'}} />
                </div>
                <div class="d-grid gap-2 col-6 mx-auto">
                  <button className="haveAcc" onClick={handleLogin} type="button"><strong> Already a member? </strong></button>
                  <button class="btn-register" type="button" onClick={handleRegister}>Register</button>
                  {regLoading && 
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
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Register;
