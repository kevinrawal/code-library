import React from 'react'
import { BrowserRouter, Routes, Route } from "react-router-dom";

import Home from './components/Home';
import LoginPage from './components/LoginPage';
import DashBoard from './components/DashBoard';
import SingInPage from './components/SingInPage';
import PageNotFound from './components/shared/PageNotFound';

function App() {
  return (
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path='/sing-in' element={<SingInPage />} />
          <Route path="/dashboard" element={<DashBoard />} />
          <Route path="*" element={<PageNotFound />} />
        </Routes>
      </BrowserRouter>
  )
};

export default App;
