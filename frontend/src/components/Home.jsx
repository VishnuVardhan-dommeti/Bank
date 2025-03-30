// src/components/HomePage.jsx
import React from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import "./Home.css";
import { FaSignInAlt, FaUserPlus, FaUniversity, FaMobileAlt, FaPiggyBank } from "react-icons/fa";

const Home = () => {
  return (
    <div className="home-container">
      {/* Navbar */}
      <nav className="navbar navbar-expand-lg navbar-dark bg-primary p-3">
        <div className="container">
          <a className="navbar-brand d-flex align-items-center" href="#">
            <FaUniversity className="me-2" /> <strong>Mthree Bank</strong>
          </a>
          <div className="ms-auto">
            <a className="btn btn-outline-light me-2" href="/login">
              <FaSignInAlt /> Login
            </a>
            <a className="btn btn-outline-light" href="/register">
              <FaUserPlus /> Register
            </a>
          </div>
        </div>
      </nav>
      
      {/* Hero Section */}
      <header className="hero-section text-center text-white">
        <div className="container">
          <h1 className="display-4">Welcome to Mthree Bank</h1>
          <p className="lead">Experience modern banking with security and convenience</p>
          <div className="mt-4">
            <a className="btn btn-lg btn-dark me-3" href="/login">
              <FaSignInAlt /> Login
            </a>
            <a className="btn btn-lg btn-outline-light" href="/register">
              <FaUserPlus /> Register
            </a>
          </div>
          <p className="mt-3">
            <a className="text-white" href="/admin">Admin Login</a>
          </p>
        </div>
      </header>
      
      {/* Features Section */}
      <section className="features container py-5">
        <div className="row text-center">
          <div className="col-md-4">
            <div className="feature-card">
              <FaUniversity className="feature-icon text-primary" />
              <h3>Secure Banking</h3>
              <p>Bank with confidence using our secure platform</p>
            </div>
          </div>
          <div className="col-md-4">
            <div className="feature-card">
              <FaMobileAlt className="feature-icon text-success" />
              <h3>Mobile Banking</h3>
              <p>Access your account anytime, anywhere</p>
            </div>
          </div>
          <div className="col-md-4">
            <div className="feature-card">
              <FaPiggyBank className="feature-icon text-warning" />
              <h3>Smart Savings</h3>
              <p>Earn interest and grow your savings</p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;
