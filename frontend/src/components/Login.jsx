import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './Login.css';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';
const Login = ({ onLoginSuccess }) => {
  const [step, setStep] = useState('email'); 
  const [email, setEmail] = useState('');
  const [name, setName] = useState('');
  const [otp, setOtp] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [isNewUser, setIsNewUser] = useState(false);
  useEffect(() => {
    document.body.style.overflow = 'hidden';
    document.body.style.background = '#ffffff';
    return () => {
      document.body.style.overflow = '';
      document.body.style.background = '';
    };
  }, []);
  const handleCheckEmail = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setSuccess(null);
    try {
      const checkResponse = await axios.post(`${API_BASE_URL}/auth/check-email`, {
        email
      });
      if (checkResponse.data.verified) {
        const { token, user } = checkResponse.data.data;
        localStorage.setItem('authToken', token);
        localStorage.setItem('user', JSON.stringify(user));
        onLoginSuccess(token, user);
      } else {
        setIsNewUser(true);
        const otpResponse = await axios.post(`${API_BASE_URL}/auth/request-otp`, {
          email
        });
        setSuccess(otpResponse.data.message);
        setStep('otp');
      }
    } catch (err) {
      setError(err.response?.data?.message || 'An error occurred. Please try again.');
    } finally {
      setLoading(false);
    }
  };
  const handleVerifyOtp = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const response = await axios.post(`${API_BASE_URL}/auth/verify-otp`, {
        email,
        otp
      });
      const { token, user } = response.data.data;
      localStorage.setItem('authToken', token);
      localStorage.setItem('user', JSON.stringify(user));
      onLoginSuccess(token, user);
    } catch (err) {
      setError(err.response?.data?.message || 'An error occurred. Please try again.');
    } finally {
      setLoading(false);
    }
  };
  const handleBackToEmail = () => {
    setStep('email');
    setOtp('');
    setError(null);
    setSuccess(null);
    setIsNewUser(false);
  };
  return (
    <div className="login-container">
      <div className="login-left">
        <div className="login-content">
          <div className="login-brand">
            <div className="brand-dot"></div>
            <span className="brand-name">SentiBot</span>
          </div>
          <div className="login-header">
            <h1>{step === 'email' ? 'Hello,' : 'Verify Your Email'}<br />{step === 'email' ? 'Welcome Back' : ''}</h1>
            <p>{step === 'email' ? 'Hey, welcome back to your special place' : 'Enter the code sent to your email'}</p>
          </div>
          {error && (
            <div className="alert alert-error">
              <span>⚠️</span>
              <span>{error}</span>
            </div>
          )}
          {success && (
            <div className="alert alert-success">
              <span>✅</span>
              <span>{success}</span>
            </div>
          )}
          {step === 'email' ? (
            <form onSubmit={handleCheckEmail} className="login-form">
              <div className="form-group">
                <input
                  type="email"
                  id="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="stanley@gmail.com"
                  required
                  disabled={loading}
                  autoFocus
                  className="form-input"
                />
              </div>
              <div className="form-group">
                <input
                  type="password"
                  id="password"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  placeholder="••••••••••••"
                  disabled={loading}
                  className="form-input"
                />
              </div>
              <div className="form-options">
                <label className="remember-me">
                  <input type="checkbox" />
                  <span>Remember me</span>
                </label>
              </div>
              <button type="submit" className="btn-signin" disabled={loading}>
                {loading ? '⏳ Checking...' : 'Sign In'}
              </button>
            </form>
          ) : (
            <form onSubmit={handleVerifyOtp} className="login-form">
              <div className="form-group">
                <p className="otp-hint">Sent to: {email}</p>
                <input
                  type="text"
                  id="otp"
                  value={otp}
                  onChange={(e) => setOtp(e.target.value.replace(/\D/g, '').slice(0, 6))}
                  placeholder="Enter 6-digit code"
                  required
                  disabled={loading}
                  maxLength="6"
                  pattern="\d{6}"
                  autoFocus
                  className="form-input otp-input"
                />
              </div>
              <button type="submit" className="btn-signin" disabled={loading || otp.length !== 6}>
                {loading ? '⏳ Verifying...' : 'Verify & Continue'}
              </button>
              <div className="login-footer">
                <button type="button" onClick={handleBackToEmail} className="back-link">
                  ← Back to Email
                </button>
                <p className="resend-hint">Didn't receive? Check spam folder</p>
              </div>
            </form>
          )}
        </div>
      </div>
      <div className="login-right">
        <img src="/login.png" alt="Login" className="login-image" />
      </div>
    </div>
  );
};
export default Login;