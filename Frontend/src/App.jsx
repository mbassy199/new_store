import { useState, useEffect } from 'react';
import { Route, Routes, BrowserRouter, Navigate } from 'react-router-dom';
import Login from './views/auth/Login';
import Register from './views/auth/Register';
import ForgotPassword from './views/auth/ForgotPassword';
import CreatePassword from './views/auth/CreatePassword';
import StoreHeader from './views/auth/base/StoreHeader';
import StoreFooter from './views/auth/base/StoreFooter';
import MainWrapper from './Layouts/MainWrapper';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    const userToken = localStorage.getItem('userToken');
    if (userToken) {
      setIsLoggedIn(true);
    }
  }, []);

  return (
    <BrowserRouter>
      <StoreHeader />
      <Routes>
        <Route
          path="/"
          element={isLoggedIn ? <Navigate to="/dashboard" replace /> : <Navigate to="/login" replace />}
        />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/forgot-password" element={<ForgotPassword />} />
        <Route path="/create-new-password" element={<CreatePassword />} />
        <Route
          path="/dashboard"
          element={isLoggedIn ? <MainWrapper /> : <Navigate to="/login" replace />}
        />
      </Routes>
      <StoreFooter />
    </BrowserRouter>
  );
}

export default App;
