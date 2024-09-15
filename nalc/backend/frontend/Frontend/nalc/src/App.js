import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Login from './Screen/Login/Login';
import Register from './Screen/Register/Register';
import Home from './Screen/Home/Home';
import UserProfile from './Screen/Profile/Profile';
import AdminScreen from './Screen/Admin/AdminScreen';
import 'ldrs/ring'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/home" element={<Home />} />
        <Route path="/profile" element={<UserProfile />} />
        <Route path="/admin" element={<AdminScreen />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
