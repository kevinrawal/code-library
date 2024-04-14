import React, { useState,useRef } from "react";
import axios from "axios";
import { Link,useNavigate } from "react-router-dom";
import { Cookies } from 'react-cookie';
import Button from "../shared/Button";

function LoginPage() {
  const username = useRef();
  const password = useRef();
  const navigate = useNavigate();
  const [warningOnLogin, setWarningOnLogin] = useState();
  const cookies = new Cookies();

  function setCookieValue(response, username){
    cookies.set('access_token', response.data.access_token, { path: '/' });
    cookies.set('refresh_token', response.data.refresh_token, { path: '/' });
    cookies.set('username', username, { path: '/' });
  }
  function authenticate(username, password) {
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);
    
    axios
      ({
          url: "http://127.0.0.1:8000/token",
          method: "post",
          data: formData
      })
      .then((response) => {
        console.log(response);
        setCookieValue(response, username);
        navigate("/dashboard");
      })
      .catch((error) => {
        console.log(error);
        setWarningOnLogin("Conection Error, please try again");
      });
  }

  function onSubmit() {
    if (username.current.value && password.current.value) {
      authenticate(username.current.value, password.current.value);
    }
    else{
      setWarningOnLogin("Please enter the username and password");
    }
  }

  return (
    <div className="login-container flex items-center justify-center min-h-screen bg-gray-100">
      <div className="login-form bg-white shadow-md rounded-lg px-8 py-6 max-w-md w-full">
        <h2 className="text-2xl font-semibold text-center mb-4">Login</h2>
        <form className="space-y-4">
          <div className="flex flex-col">

            <label htmlFor="username" className="text-sm font-medium mb-1">Username</label>
            <input
              type="text"
              id="username"
              ref={username}
              className="shadow appearance-none border rounded-md w-full py-2 px-3 text-gray-700 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            />
          </div>
          <div className="flex flex-col">
            <label htmlFor="password" className="text-sm font-medium mb-1">Password</label>
            <input
              type="password"
              id="password"
              ref={password}
              className="shadow appearance-none border rounded-md w-full py-2 px-3 text-gray-700 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            />
          </div>

          {warningOnLogin && (
            <p className="text-red-500 text-sm font-medium">{warningOnLogin}</p>
          )}

          <Button title="Login" onClickFunction={onSubmit}/>
        </form>

        <div className="flex mt-4 items-center justify-between text-sm">
          <Link to="/auth/forgot-password" className="text-indigo-600 hover:text-indigo-800">Forgot Password?</Link>
          <Link to="/auth/sing-in" className="text-indigo-600 hover:text-indigo-800">Create Account</Link>
        </div>
      </div>
    </div>
  );
}

export default LoginPage;

