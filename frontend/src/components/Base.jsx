import React from "react";
import { Link } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";
import "./Base.css"; // External CSS file for global styling

const Base = ({ children, user }) => {
  return (
    <div className="base-container">
      <nav className="navbar navbar-expand-lg navbar-dark">
        <div className="container">
          <Link className="navbar-brand" to={user ? `/dashboard/${user.username}` : "/"}>
            <i className="fas fa-university me-2"></i> Mthree Bank
          </Link>
          <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
            <span className="navbar-toggler-icon"></span>
          </button>
          <div className="collapse navbar-collapse" id="navbarNav">
            <ul className="navbar-nav ms-auto">
              {user ? (
                <>
                  <li className="nav-item">
                    <Link className="nav-link" to={`/dashboard/${user.username}`}>
                      <i className="fas fa-home me-1"></i> Dashboard
                    </Link>
                  </li>
                  <li className="nav-item">
                    <Link className="nav-link" to={`/profile/${user.username}`}>
                      <i className="fas fa-info-circle me-1"></i> About
                    </Link>
                  </li>
                  <li className="nav-item dropdown profile-dropdown">
                    <Link className="nav-link dropdown-toggle" to="#" id="profileDropdown">
                      <i className="fas fa-user me-1"></i> Profile
                    </Link>
                    <ul className="dropdown-menu dropdown-menu-end" aria-labelledby="profileDropdown">
                      <li><Link className="dropdown-item" to={`/profile/${user.username}`}><i className="fas fa-user-circle me-2"></i>My Profile</Link></li>
                      <li><Link className="dropdown-item" to={`/settings/${user.username}`}><i className="fas fa-cog me-2"></i>Settings</Link></li>
                    </ul>
                  </li>
                  <li className="nav-item">
                    <Link className="nav-link" to="/logout">
                      <i className="fas fa-sign-out-alt me-1"></i> Logout
                    </Link>
                  </li>
                </>
              ) : (
                <>
                  <li className="nav-item">
                    <Link className="nav-link" to="/about">
                      <i className="fas fa-info-circle me-1"></i> About
                    </Link>
                  </li>
                  <li className="nav-item">
                    <Link className="nav-link" to="/login">
                      <i className="fas fa-sign-in-alt me-1"></i> Login
                    </Link>
                  </li>
                  <li className="nav-item">
                    <Link className="nav-link" to="/register">
                      <i className="fas fa-user-plus me-1"></i> Register
                    </Link>
                  </li>
                </>
              )}
            </ul>
          </div>
        </div>
      </nav>
      <main className="content">{children}</main>
    </div>
  );
};

export default Base;
