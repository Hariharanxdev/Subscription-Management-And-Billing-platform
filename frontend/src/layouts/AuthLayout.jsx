import { Outlet } from "react-router-dom";
import "../assets/styles/auth.css";

const AuthLayout = () => {
  return (
    <div className="auth-container">

      {/* Background Blur */}
      <div className="blur blur1"></div>
      <div className="blur blur2"></div>
      <div className="blur blur3"></div>

      {/* Logo */}

      <div className="logo-section">

        <div className="logo-circle">
          N
        </div>

        <h1>NovaBill</h1>

        <p>
          Subscription Management Platform
        </p>

      </div>

      {/* Card */}

      <div className="auth-card">

        <Outlet />

      </div>

    </div>
  );
};

export default AuthLayout;