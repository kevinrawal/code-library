import React from "react";
import { Link, Outlet } from "react-router-dom";

function Auth() {
    return (
        <div>
            <Outlet />
        </div>
    );
}

export default Auth;