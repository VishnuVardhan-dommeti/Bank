import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Base from "./components/Base";
import Home from "./components/Home";
import Register from "./components/Register";

const App = () => {
  return (
    <Router>
      <Base>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<div>Login Page</div>} />
          <Route path="/register" element={<Register />} />
          <Route path="/admin" element={<div>Admin Login</div>} />
        </Routes>
      </Base>
    </Router>
  );
};

export default App;