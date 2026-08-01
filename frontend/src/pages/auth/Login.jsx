import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import {
  FaEnvelope,
  FaLock
} from "react-icons/fa";
import {
  IoEyeOutline,
  IoEyeOffOutline
} from "react-icons/io5";

import { toast } from "react-hot-toast";
import { jwtDecode } from "jwt-decode";
import { loginUser } from "../../services/authService";

const Login = () => {
  const navigate = useNavigate();

  const [showPassword, setShowPassword] = useState(false);

  const [loading, setLoading] = useState(false);

  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleLogin = async (e) => {
    e.preventDefault();

    if (!formData.email || !formData.password) {
      toast.error("Please fill all fields");
      return;
    }

    try {
      setLoading(true);

      const data = await loginUser(
        formData.email,
        formData.password
      );

      localStorage.setItem(
        "access_token",
        data.access_token
      );

      const decoded = jwtDecode(data.access_token);

      toast.success("Login Successful");

      if (decoded.role === "admin") {
        navigate("/admin/dashboard");
      } else {
        navigate("/customer/dashboard");
      }

    } catch (error) {

      toast.error(
        error.response?.data?.detail || "Login Failed"
      );

    } finally {

      setLoading(false);

    }
  };

  return (
    <>
      <h2>Welcome Back </h2>

      <p>Login to your NovaBill account</p>

      <form onSubmit={handleLogin}>

        <div className="input-group">
          <label>Email</label>

          <div className="input-box">
            <FaEnvelope />

            <input
              type="email"
              name="email"
              placeholder="Enter your email"
              value={formData.email}
              onChange={handleChange}
            />
          </div>
        </div>

        <div className="input-group">
          <label>Password</label>

          <div className="input-box">
            <FaLock />

            <input
              type={showPassword ? "text" : "password"}
              name="password"
              placeholder="Enter your password"
              value={formData.password}
              onChange={handleChange}
            />

            <span
              style={{
                cursor: "pointer",
                color: "#fff"
              }}
              onClick={() =>
                setShowPassword(!showPassword)
              }
            >
              {showPassword ? (
                <IoEyeOffOutline />
              ) : (
                <IoEyeOutline />
              )}
            </span>

          </div>
        </div>

        <div className="login-options">

          <label>
            <input type="checkbox" /> Remember Me
          </label>

          <Link to="#">
            Forgot Password?
          </Link>

        </div>

        <button
          type="submit"
          className="login-btn"
        >
          {loading ? "Signing In..." : "Login"}
        </button>

      </form>

      <p className="bottom-text">

        Don't have an account?

        <Link to="/register">
          Create Account
        </Link>

      </p>
    </>
  );
};

export default Login;