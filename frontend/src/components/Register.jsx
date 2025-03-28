import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const Register = () => {
    const [formData, setFormData] = useState({
        first_name: "",
        last_name: "",
        email: "",
        phone: "",
        date_of_birth: "",
        national_id: "",
        gender: "",
        marital_status: "",
        occupation: "",
        income: "",
        address: "",
        city: "",
        state: "",
        zip_code: "",
        account_type: "",
        branch: "",
        opening_date: "",
        balance_amount: "",
        password: "",
        confirm_password: "",
        otp: "",
    });

    const [otpSent, setOtpSent] = useState(false);
    const navigate = useNavigate();

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleOTP = async () => {
        if (!formData.email) {
            alert("Please enter an email address first!");
            return;
        }
        try {
            const response = await axios.post("/api/send-otp/", { email: formData.email }, {
                headers: { "Content-Type": "application/json" }
            });
            if (response.data.success) {
                setOtpSent(true);
                alert("OTP sent to your email!");
            } else {
                alert("Error sending OTP: " + response.data.message);
            }
        } catch (error) {
            alert("Failed to send OTP.");
        }
    };
    

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (formData.password !== formData.confirm_password) {
            alert("Passwords do not match!");
            return;
        }
        try {
            const response = await axios.post("/api/register/", formData);
            if (response.data.success) {
                alert("Registration successful!");
                navigate("/login");
            } else {
                alert("Error: " + response.data.message);
            }
        } catch (error) {
            alert("Failed to register.");
        }
    };

    return (
        <div className="container">
            <div className="row justify-content-center">
                <div className="col-md-8">
                    <div className="card shadow-sm">
                        <div className="card-header">
                            <h3 className="mb-0">Create New Account</h3>
                        </div>
                        <div className="card-body p-4">
                            <form onSubmit={handleSubmit}>
                                <div className="row">
                                    <div className="col-md-6 mb-3">
                                        <label className="form-label">First Name</label>
                                        <input type="text" name="first_name" className="form-control" required onChange={handleChange} />
                                    </div>
                                    <div className="col-md-6 mb-3">
                                        <label className="form-label">Last Name</label>
                                        <input type="text" name="last_name" className="form-control" required onChange={handleChange} />
                                    </div>
                                </div>

                                <div className="row">
                                    <div className="col-md-6 mb-3">
                                        <label className="form-label">Email Address</label>
                                        <input type="email" name="email" className="form-control" required onChange={handleChange} />
                                    </div>
                                    <div className="col-md-6 mb-3">
                                        <label className="form-label">Phone Number</label>
                                        <input type="text" name="phone" className="form-control" required onChange={handleChange} />
                                    </div>
                                </div>

                                <div className="row">
                                    <div className="col-md-6 mb-3">
                                        <label className="form-label">Date of Birth</label>
                                        <input type="date" name="date_of_birth" className="form-control" required onChange={handleChange} />
                                    </div>
                                    <div className="col-md-6 mb-3">
                                        <label className="form-label">National ID</label>
                                        <input type="text" name="national_id" className="form-control" required onChange={handleChange} />
                                    </div>
                                </div>

                                <div className="row">
                                    <div className="col-md-6 mb-3">
                                        <label className="form-label">Gender</label>
                                        <select name="gender" className="form-select" required onChange={handleChange}>
                                            <option value="">Select</option>
                                            <option value="Male">Male</option>
                                            <option value="Female">Female</option>
                                            <option value="Other">Other</option>
                                        </select>
                                    </div>
                                    <div className="col-md-6 mb-3">
                                        <label className="form-label">Marital Status</label>
                                        <select name="marital_status" className="form-select" required onChange={handleChange}>
                                            <option value="">Select</option>
                                            <option value="Single">Single</option>
                                            <option value="Married">Married</option>
                                        </select>
                                    </div>
                                </div>

                                <div className="mb-3">
                                    <label className="form-label">Occupation</label>
                                    <input type="text" name="occupation" className="form-control" required onChange={handleChange} />
                                </div>

                                <div className="mb-3">
                                    <label className="form-label">Income</label>
                                    <input type="number" name="income" className="form-control" required onChange={handleChange} />
                                </div>

                                <div className="mb-3">
                                    <label className="form-label">Address</label>
                                    <textarea name="address" className="form-control" required onChange={handleChange}></textarea>
                                </div>

                                <div className="row">
                                    <div className="col-md-4 mb-3">
                                        <label className="form-label">City</label>
                                        <input type="text" name="city" className="form-control" required onChange={handleChange} />
                                    </div>
                                    <div className="col-md-4 mb-3">
                                        <label className="form-label">State</label>
                                        <input type="text" name="state" className="form-control" required onChange={handleChange} />
                                    </div>
                                    <div className="col-md-4 mb-3">
                                        <label className="form-label">ZIP Code</label>
                                        <input type="text" name="zip_code" className="form-control" required onChange={handleChange} />
                                    </div>
                                </div>

                                <div className="mb-3">
                                    <label className="form-label">Account Type</label>
                                    <select name="account_type" className="form-select" required onChange={handleChange}>
                                        <option value="">Select</option>
                                        <option value="savings">Savings Account</option>
                                        <option value="current">Current Account</option>
                                    </select>
                                </div>

                                <div className="mb-3">
                                    <label className="form-label">Branch</label>
                                    <input type="text" name="branch" className="form-control" required onChange={handleChange} />
                                </div>

                                <div className="mb-3">
                                    <label className="form-label">Opening Date</label>
                                    <input type="date" name="opening_date" className="form-control" required onChange={handleChange} />
                                </div>

                                <div className="mb-3">
                                    <label className="form-label">Password</label>
                                    <input type="password" name="password" className="form-control" required onChange={handleChange} />
                                </div>

                                <button type="button" className="btn btn-secondary mb-3" onClick={handleOTP}>Verify Email</button>

                                {otpSent && (
                                    <div className="mb-3">
                                        <label className="form-label">Enter OTP</label>
                                        <input type="text" name="otp" className="form-control" required onChange={handleChange} />
                                    </div>
                                )}

                                <button type="submit" className="btn btn-primary w-100">Create Account</button>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Register;
