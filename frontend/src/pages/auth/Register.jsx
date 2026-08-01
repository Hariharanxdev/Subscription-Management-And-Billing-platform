import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import {
  FaUser,
  FaEnvelope,
  FaLock
} from "react-icons/fa";
import {
  IoEyeOutline,
  IoEyeOffOutline
} from "react-icons/io5";

import { toast } from "react-hot-toast";
import { registerUser } from "../../services/authService";

const Register = () => {
  const navigate = useNavigate();

  const [showPassword, setShowPassword] = useState(false);
  const [showConfirm, setShowConfirm] = useState(false);

  const [loading, setLoading] = useState(false);

  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
    confirmPassword: "",
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleRegister = async (e) => {
    e.preventDefault();

    if (
      !formData.username ||
      !formData.email ||
      !formData.password ||
      !formData.confirmPassword
    ) {
      toast.error("Please fill all fields");
      return;
    }

    if (formData.password !== formData.confirmPassword) {
      toast.error("Passwords do not match");
      return;
    }

    try {
      setLoading(true);

      await registerUser({
        username: formData.username,
        email: formData.email,
        password: formData.password,
      });

      toast.success("Account Created Successfully");

      navigate("/login");

    } catch (error) {

      toast.error(
        error.response?.data?.detail ||
        "Registration Failed"
      );

    } finally {

      setLoading(false);

    }
  };

  return (
    <>
      <h2>Create Account </h2>

      <p>Create your NovaBill account</p>

      <form onSubmit={handleRegister}>

        <div className="input-group">
          <label>Username</label>

          <div className="input-box">
            <FaUser />

            <input
              type="text"
              name="username"
              placeholder="Enter username"
              value={formData.username}
              onChange={handleChange}
            />
          </div>
        </div>

        <div className="input-group">
          <label>Email</label>

          <div className="input-box">
            <FaEnvelope />

            <input
              type="email"
              name="email"
              placeholder="Enter email"
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
              placeholder="Enter password"
              value={formData.password}
              onChange={handleChange}
            />

            <span
              onClick={() => setShowPassword(!showPassword)}
              style={{ cursor: "pointer", color: "#fff" }}
            >
              {showPassword ? <IoEyeOffOutline /> : <IoEyeOutline />}
            </span>

          </div>
        </div>

        <div className="input-group">
          <label>Confirm Password</label>

          <div className="input-box">
            <FaLock />

            <input
              type={showConfirm ? "text" : "password"}
              name="confirmPassword"
              placeholder="Confirm password"
              value={formData.confirmPassword}
              onChange={handleChange}
            />

            <span
              onClick={() => setShowConfirm(!showConfirm)}
              style={{ cursor: "pointer", color: "#fff" }}
            >
              {showConfirm ? <IoEyeOffOutline /> : <IoEyeOutline />}
            </span>

          </div>
        </div>

        <button
          type="submit"
          className="login-btn"
        >
          {loading ? "Creating..." : "Create Account"}
        </button>

      </form>

      <p className="bottom-text">
        Already have an account?
        <Link to="/login"> Login</Link>
      </p>
    </>
  );
};

export default Register;