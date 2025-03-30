import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

const Register = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    first_name: "",
    last_name: "",
    email: "",
    phone: "",
    dob: "",
    gender: "",
    occupation: "",
    income: "",
    address: "",
    city: "",
    state: "",
    zip_code: "",
    country: "",
    account_type: "",
    branch: "",
    balance: "",
    password: "",
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post("http://127.0.0.1:8000/api/register/", formData);
      alert("Registration Successful!");
      navigate("/login");
    } catch (error) {
      alert("Error during registration");
    }
  };

  return (
    <div className="container mt-5">
      <h2 className="text-center mb-4">Register</h2>
      <form onSubmit={handleSubmit} className="border p-4 shadow rounded">
        <div className="row">
          {[
            { name: "first_name", label: "First Name" },
            { name: "last_name", label: "Last Name" },
            { name: "email", label: "Email" },
            { name: "phone", label: "Phone" },
            { name: "dob", label: "Date of Birth", type: "date" },
            { name: "occupation", label: "Occupation" },
            { name: "income", label: "Income", type: "number" },
            { name: "address", label: "Street Address" },
            { name: "city", label: "City" },
            { name: "state", label: "State" },
            { name: "zip_code", label: "Zip Code" },
            { name: "country", label: "Country" },
            { name: "balance", label: "Entry Deposit", type: "number" },
            { name: "password", label: "Password", type: "password" },
          ].map((field) => (
            <div key={field.name} className="col-md-6 mb-3">
              <label>{field.label}</label>
              <input
                type={field.type || "text"}
                name={field.name}
                className="form-control"
                onChange={handleChange}
                required
              />
            </div>
          ))}

          <div className="col-md-6 mb-3">
            <label>Gender</label>
            <select name="gender" className="form-control" onChange={handleChange} required>
              <option value="">Select</option>
              <option value="Male">Male</option>
              <option value="Female">Female</option>
              <option value="Other">Other</option>
            </select>
          </div>

          <div className="col-md-6 mb-3">
            <label>Account Type</label>
            <select name="account_type" className="form-control" onChange={handleChange} required>
              <option value="">Select</option>
              <option value="Savings">Savings</option>
              <option value="Current">Current</option>
            </select>
          </div>

          <div className="col-md-6 mb-3">
            <label>Branch</label>
            <select name="branch" className="form-control" onChange={handleChange} required>
              <option value="">Select</option>
              <option value="1">Main Branch</option>
              <option value="2">City Branch</option>
            </select>
          </div>
        </div>
        <button type="submit" className="btn btn-primary w-100">Register</button>
      </form>
    </div>
  );
};

export default Register;
