import React from 'react'
import { BrowserRouter, Routes, Route } from "react-router-dom";

import Home from './components/Home';
import DashBoard from './components/DashBoard';
import Auth from './components/auth/Auth';
import LoginPage from './components/auth/LoginPage';
import SingInPage from './components/auth/SingInPage';
import PageNotFound from './components/shared/PageNotFound';
import ForgotPassword from './components/auth/ForgotPassword';

function App() {
  return (
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/auth" element={<Auth />}>
            <Route index element={<LoginPage />} />
            <Route path="login" element={<LoginPage />} />
            <Route path="sing-in" element={<SingInPage />} />
            <Route path="forgot-password" element={<ForgotPassword />} />
          </Route>
          <Route path="/dashboard" element={<DashBoard />} />
          <Route path="*" element={<PageNotFound />} />
        </Routes>
      </BrowserRouter>
  )
}

export default App;
