import React from "react";
import { Link } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";
import "./Home.css"; // Import the updated CSS file

const Home = () => {
  return (
    <div className="home-container text-center">
      <div className="home-content p-5">
        <h1 className="text-gradient">Welcome to Mthree Bank</h1>
        <p className="text-dark">Experience modern banking with security and convenience</p>
        <div className="mt-4">
          <Link to="/login" className="btn btn-primary me-2">
            <i className="fas fa-sign-in-alt"></i> LOGIN
          </Link>
          <Link to="/register" className="btn btn-outline-light">
            <i className="fas fa-user-plus"></i> REGISTER
          </Link>
          <br />
          <Link to="/admin" className="mt-2 d-block text-dark text-decoration-none">Admin Login</Link>
        </div>

        <div className="row mt-5">
          <div className="col-md-4">
            <div className="card custom-card">
              <i className="fas fa-shield-alt fa-3x icon-style"></i>
              <h4 className="mt-3">Secure Banking</h4>
              <p>Bank with confidence using our secure platform</p>
            </div>
          </div>
          <div className="col-md-4">
            <div className="card custom-card">
              <i className="fas fa-mobile-alt fa-3x icon-style"></i>
              <h4 className="mt-3">Mobile Banking</h4>
              <p>Access your account anytime, anywhere</p>
            </div>
          </div>
          <div className="col-md-4">
            <div className="card custom-card">
              <i className="fas fa-chart-line fa-3x icon-style"></i>
              <h4 className="mt-3">Smart Savings</h4>
              <p>Earn interest and grow your savings</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;
