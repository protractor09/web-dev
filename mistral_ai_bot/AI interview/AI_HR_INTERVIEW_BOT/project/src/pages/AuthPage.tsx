import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useAuth } from '../hooks/useAuth';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { Bot, Mail, Lock, User, Phone, Building, ArrowRight, Sparkles, Shield, Eye, EyeOff } from 'lucide-react';
import LoadingSpinner from '../components/LoadingSpinner';
import ThreeDBackground from '../components/3DBackground';
import Confetti from 'react-confetti';

const AuthPage: React.FC = () => {
  const [searchParams] = useSearchParams();
  const role = (searchParams.get('role') as 'candidate' | 'hr') || 'candidate';
  
  const [isSignUp, setIsSignUp] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    password: '',
    company: ''
  });
  const [otp, setOtp] = useState('');
  const [showOtpVerification, setShowOtpVerification] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [showConfetti, setShowConfetti] = useState(false);
  
  const { login, signup, verifyOTP, sendOTP } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (success) {
      setShowConfetti(true);
      setTimeout(() => setShowConfetti(false), 3000);
    }
  }, [success]);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData(prev => ({
      ...prev,
      [e.target.name]: e.target.value
    }));
    setError('');
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    try {
      if (isSignUp) {
        const result = await signup(
          formData.name, 
          formData.email, 
          formData.phone, 
          formData.password, 
          role,
          role === 'hr' ? formData.company : undefined
        );
        
        if (result.success && result.needsVerification) {
          setShowOtpVerification(true);
          setSuccess('OTP sent successfully! Please check your email/phone.');
        } else {
          setError(result.message || 'Signup failed');
        }
      } else {
        const success = await login(formData.email, formData.password, role);
        
        if (success) {
          setSuccess('Login successful!');
          setTimeout(() => {
            if (role === 'hr') {
              navigate('/hr-dashboard');
            } else {
              navigate('/student-info');
            }
          }, 1500);
        } else {
          setError('Invalid credentials or user not found. Please sign up first.');
        }
      }
    } catch (err) {
      setError('An unexpected error occurred. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleOtpVerification = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    try {
      const success = await verifyOTP(formData.email, otp);
      
      if (success) {
        setSuccess('Account verified successfully! You can now sign in.');
        setShowOtpVerification(false);
        setIsSignUp(false);
        setFormData(prev => ({ ...prev, name: '', phone: '', password: '', company: '' }));
        setOtp('');
      } else {
        setError('Invalid or expired OTP. Please try again.');
      }
    } catch (err) {
      setError('OTP verification failed. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const resendOtp = async () => {
    setIsLoading(true);
    try {
      await sendOTP(formData.email);
      setSuccess('OTP resent successfully!');
    } catch (err) {
      setError('Failed to resend OTP. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const toggleMode = () => {
    setIsSignUp(!isSignUp);
    setError('');
    setSuccess('');
    setShowOtpVerification(false);
    setFormData({ name: '', email: '', phone: '', password: '', company: '' });
    setOtp('');
  };

  return (
    <div className="min-h-screen animated-bg flex items-center justify-center p-4 relative overflow-hidden">
      <ThreeDBackground />
      {showConfetti && <Confetti recycle={false} numberOfPieces={200} />}
      
      {/* Back to Home */}
      <motion.button
        onClick={() => navigate('/')}
        className="absolute top-6 left-6 z-20 glass rounded-xl p-3 border border-white/10 text-white hover:bg-white/10 transition-all duration-200"
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
      >
        <ArrowRight className="h-5 w-5 rotate-180" />
      </motion.button>

      <div className="max-w-md w-full relative z-10">
        
        {/* Role Indicator */}
        <motion.div
          initial={{ y: -20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          className="text-center mb-6"
        >
          <div className={`inline-flex items-center justify-center w-16 h-16 ${
            role === 'hr' ? 'bg-gradient-to-r from-green-500 to-emerald-600' : 'bg-gradient-to-r from-cyber-blue to-purple-600'
          } rounded-2xl mb-4 shadow-2xl ${role === 'hr' ? 'glow-green' : 'glow-blue'}`}>
            {role === 'hr' ? <Building className="h-8 w-8 text-white" /> : <Bot className="h-8 w-8 text-white" />}
          </div>
          <h1 className="text-2xl font-bold text-white mb-2 font-orbitron">
            {role === 'hr' ? 'HR DASHBOARD' : 'AI INTERVIEWER'}
          </h1>
          <p className="text-gray-300">
            {role === 'hr' ? 'Manage interviews and candidates' : 'Practice with AI-powered interviews'}
          </p>
        </motion.div>

        <motion.div
          initial={{ x: 100, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          transition={{ duration: 0.8, ease: "easeOut" }}
          className="glass rounded-3xl p-8 border border-white/10 shadow-2xl"
        >
          
          {/* OTP Verification */}
          <AnimatePresence>
            {showOtpVerification ? (
              <motion.div
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.9 }}
              >
                <div className="text-center mb-8">
                  <Shield className="h-12 w-12 text-cyber-blue mx-auto mb-4" />
                  <h2 className="text-2xl font-bold text-white mb-2">Verify Your Account</h2>
                  <p className="text-gray-400">Enter the OTP sent to {formData.email}</p>
                </div>

                <form onSubmit={handleOtpVerification} className="space-y-6">
                  <div>
                    <label htmlFor="otp" className="block text-sm font-medium text-gray-300 mb-2">
                      Enter OTP
                    </label>
                    <input
                      id="otp"
                      type="text"
                      value={otp}
                      onChange={(e) => setOtp(e.target.value)}
                      className="w-full px-4 py-3 bg-dark-200/50 border border-white/10 rounded-xl text-white text-center text-2xl font-mono tracking-widest placeholder-gray-400 focus:ring-2 focus:ring-cyber-blue focus:border-cyber-blue transition-all duration-200"
                      placeholder="000000"
                      maxLength={6}
                      required
                    />
                  </div>

                  {error && (
                    <motion.div
                      initial={{ opacity: 0, y: -10 }}
                      animate={{ opacity: 1, y: 0 }}
                      className="bg-red-500/10 border border-red-500/20 rounded-xl p-3"
                    >
                      <p className="text-red-400 text-sm">{error}</p>
                    </motion.div>
                  )}

                  {success && (
                    <motion.div
                      initial={{ opacity: 0, y: -10 }}
                      animate={{ opacity: 1, y: 0 }}
                      className="bg-green-500/10 border border-green-500/20 rounded-xl p-3"
                    >
                      <p className="text-green-400 text-sm">{success}</p>
                    </motion.div>
                  )}

                  <div className="space-y-3">
                    <motion.button
                      type="submit"
                      disabled={isLoading || otp.length !== 6}
                      className="w-full bg-gradient-to-r from-cyber-blue to-purple-600 text-white py-3 px-4 rounded-xl font-medium hover:from-blue-600 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-cyber-blue focus:ring-offset-2 focus:ring-offset-dark-100 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 btn-futuristic flex items-center justify-center space-x-2 glow-blue"
                      whileHover={{ scale: 1.02 }}
                      whileTap={{ scale: 0.98 }}
                    >
                      {isLoading ? <LoadingSpinner size="sm" /> : (
                        <>
                          <Shield className="h-4 w-4" />
                          <span>Verify Account</span>
                        </>
                      )}
                    </motion.button>

                    <button
                      type="button"
                      onClick={resendOtp}
                      disabled={isLoading}
                      className="w-full text-cyber-blue hover:text-white transition-colors text-sm"
                    >
                      Resend OTP
                    </button>
                  </div>
                </form>
              </motion.div>
            ) : (
              <motion.div
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.9 }}
              >
                {/* Form Header */}
                <div className="text-center mb-8">
                  <h2 className="text-2xl font-bold text-white mb-2 font-orbitron">
                    {isSignUp ? 'CREATE ACCOUNT' : 'WELCOME BACK'}
                  </h2>
                  <p className="text-gray-400">
                    {isSignUp ? 'Join the future of interviews' : 'Continue your journey'}
                  </p>
                </div>

                {/* Auth Toggle Buttons */}
                <div className="flex bg-dark-200/50 rounded-xl p-1 mb-6">
                  <button
                    type="button"
                    onClick={() => !isSignUp && toggleMode()}
                    className={`flex-1 py-2 px-4 rounded-lg text-sm font-medium transition-all duration-300 ${
                      !isSignUp 
                        ? `bg-gradient-to-r ${role === 'hr' ? 'from-green-500 to-emerald-600' : 'from-cyber-blue to-purple-600'} text-white shadow-lg` 
                        : 'text-gray-400 hover:text-white'
                    }`}
                  >
                    Sign In
                  </button>
                  <button
                    type="button"
                    onClick={() => isSignUp && toggleMode()}
                    className={`flex-1 py-2 px-4 rounded-lg text-sm font-medium transition-all duration-300 ${
                      isSignUp 
                        ? `bg-gradient-to-r ${role === 'hr' ? 'from-green-500 to-emerald-600' : 'from-cyber-blue to-purple-600'} text-white shadow-lg` 
                        : 'text-gray-400 hover:text-white'
                    }`}
                  >
                    Sign Up
                  </button>
                </div>

                {/* Form */}
                <form onSubmit={handleSubmit} className="space-y-6">
                  {isSignUp && (
                    <motion.div
                      initial={{ height: 0, opacity: 0 }}
                      animate={{ height: 'auto', opacity: 1 }}
                      exit={{ height: 0, opacity: 0 }}
                      transition={{ duration: 0.3 }}
                    >
                      <label htmlFor="name" className="block text-sm font-medium text-gray-300 mb-2">
                        Full Name *
                      </label>
                      <div className="relative">
                        <User className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
                        <input
                          id="name"
                          name="name"
                          type="text"
                          value={formData.name}
                          onChange={handleInputChange}
                          className="w-full pl-10 pr-4 py-3 bg-dark-200/50 border border-white/10 rounded-xl text-white placeholder-gray-400 focus:ring-2 focus:ring-cyber-blue focus:border-cyber-blue transition-all duration-200"
                          placeholder="Enter your full name"
                          required={isSignUp}
                        />
                      </div>
                    </motion.div>
                  )}

                  <div>
                    <label htmlFor="email" className="block text-sm font-medium text-gray-300 mb-2">
                      Email Address *
                    </label>
                    <div className="relative">
                      <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
                      <input
                        id="email"
                        name="email"
                        type="email"
                        value={formData.email}
                        onChange={handleInputChange}
                        className="w-full pl-10 pr-4 py-3 bg-dark-200/50 border border-white/10 rounded-xl text-white placeholder-gray-400 focus:ring-2 focus:ring-cyber-blue focus:border-cyber-blue transition-all duration-200"
                        placeholder="Enter your email"
                        required
                      />
                    </div>
                  </div>

                  {isSignUp && (
                    <motion.div
                      initial={{ height: 0, opacity: 0 }}
                      animate={{ height: 'auto', opacity: 1 }}
                      exit={{ height: 0, opacity: 0 }}
                      transition={{ duration: 0.3 }}
                    >
                      <label htmlFor="phone" className="block text-sm font-medium text-gray-300 mb-2">
                        Phone Number *
                      </label>
                      <div className="relative">
                        <Phone className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
                        <input
                          id="phone"
                          name="phone"
                          type="tel"
                          value={formData.phone}
                          onChange={handleInputChange}
                          className="w-full pl-10 pr-4 py-3 bg-dark-200/50 border border-white/10 rounded-xl text-white placeholder-gray-400 focus:ring-2 focus:ring-cyber-blue focus:border-cyber-blue transition-all duration-200"
                          placeholder="+1 (555) 123-4567"
                          required={isSignUp}
                        />
                      </div>
                    </motion.div>
                  )}

                  {isSignUp && role === 'hr' && (
                    <motion.div
                      initial={{ height: 0, opacity: 0 }}
                      animate={{ height: 'auto', opacity: 1 }}
                      exit={{ height: 0, opacity: 0 }}
                      transition={{ duration: 0.3 }}
                    >
                      <label htmlFor="company" className="block text-sm font-medium text-gray-300 mb-2">
                        Company Name *
                      </label>
                      <div className="relative">
                        <Building className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
                        <input
                          id="company"
                          name="company"
                          type="text"
                          value={formData.company}
                          onChange={handleInputChange}
                          className="w-full pl-10 pr-4 py-3 bg-dark-200/50 border border-white/10 rounded-xl text-white placeholder-gray-400 focus:ring-2 focus:ring-cyber-blue focus:border-cyber-blue transition-all duration-200"
                          placeholder="Enter your company name"
                          required={isSignUp && role === 'hr'}
                        />
                      </div>
                    </motion.div>
                  )}

                  <div>
                    <label htmlFor="password" className="block text-sm font-medium text-gray-300 mb-2">
                      Password *
                    </label>
                    <div className="relative">
                      <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
                      <input
                        id="password"
                        name="password"
                        type={showPassword ? 'text' : 'password'}
                        value={formData.password}
                        onChange={handleInputChange}
                        className="w-full pl-10 pr-12 py-3 bg-dark-200/50 border border-white/10 rounded-xl text-white placeholder-gray-400 focus:ring-2 focus:ring-cyber-blue focus:border-cyber-blue transition-all duration-200"
                        placeholder="Enter your password"
                        required
                        minLength={6}
                      />
                      <button
                        type="button"
                        onClick={() => setShowPassword(!showPassword)}
                        className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-white transition-colors"
                      >
                        {showPassword ? <EyeOff className="h-5 w-5" /> : <Eye className="h-5 w-5" />}
                      </button>
                    </div>
                  </div>

                  {error && (
                    <motion.div
                      initial={{ opacity: 0, y: -10 }}
                      animate={{ opacity: 1, y: 0 }}
                      className="bg-red-500/10 border border-red-500/20 rounded-xl p-3"
                    >
                      <p className="text-red-400 text-sm">{error}</p>
                    </motion.div>
                  )}

                  {success && (
                    <motion.div
                      initial={{ opacity: 0, y: -10 }}
                      animate={{ opacity: 1, y: 0 }}
                      className="bg-green-500/10 border border-green-500/20 rounded-xl p-3"
                    >
                      <p className="text-green-400 text-sm">{success}</p>
                    </motion.div>
                  )}

                  <motion.button
                    type="submit"
                    disabled={isLoading}
                    className={`w-full bg-gradient-to-r ${
                      role === 'hr' ? 'from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 glow-green' : 'from-cyber-blue to-purple-600 hover:from-blue-600 hover:to-purple-700 glow-blue'
                    } text-white py-3 px-4 rounded-xl font-medium focus:outline-none focus:ring-2 focus:ring-cyber-blue focus:ring-offset-2 focus:ring-offset-dark-100 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 btn-futuristic flex items-center justify-center space-x-2`}
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                  >
                    {isLoading ? (
                      <LoadingSpinner size="sm" />
                    ) : (
                      <>
                        <span>{isSignUp ? 'Create Account' : 'Sign In'}</span>
                        <ArrowRight className="h-4 w-4" />
                      </>
                    )}
                  </motion.button>
                </form>

                {/* Demo Info */}
                <div className="mt-6 pt-6 border-t border-white/10">
                  <p className="text-center text-sm text-gray-400">
                    <Sparkles className="inline h-4 w-4 mr-1" />
                    {isSignUp ? 'Create account to get started' : 'Demo: Use any registered email and password'}
                  </p>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </motion.div>
      </div>
    </div>
  );
};

export default AuthPage;