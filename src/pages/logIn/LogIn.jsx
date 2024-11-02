import React, { useState } from 'react';
import './LogIn.css';
import Button from '../../components/button/button';
import { motion } from 'framer-motion';
import { CognitoUser, AuthenticationDetails } from 'amazon-cognito-identity-js';
import Userpool from '../signUp/Userpool';

export const LogIn = () => {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [confirmationCode, setConfirmationCode] = useState(""); // New state for confirmation code
    const [showConfirmationInput, setShowConfirmationInput] = useState(false); // Track if confirmation input should show
    const [errorMessages, setErrorMessages] = useState("");
    const [successMessage, setSuccessMessage] = useState("");

    const onSubmit = (event) => {
        event.preventDefault();

        const user = new CognitoUser({
            Username: email,
            Pool: Userpool
        });

        const authDetails = new AuthenticationDetails({
            Username: email,
            Password: password
        });

        user.authenticateUser(authDetails, {
            onSuccess: data => {
                console.log("onSuccess:", data);
                setErrorMessages("");
                setSuccessMessage("Login successful!");
                const userId = data.idToken.payload.sub;
                localStorage.setItem("user_id", userId); // Store in localStorage for later retrieval
        
            },
            onFailure: err => {
                console.error("onFailure:", err);

                if (err.code === 'UserNotConfirmedException') {
                    setErrorMessages("Your account is not confirmed. Check your email for a confirmation code.");
                    setShowConfirmationInput(true); // Show confirmation input
                    user.resendConfirmationCode((err, result) => {
                        if (err) {
                            console.error("Error resending confirmation code:", err);
                            setErrorMessages("Failed to resend confirmation code. Try again later.");
                        } else {
                            setErrorMessages("A new confirmation code has been sent to your email.");
                        }
                    });
                } else {
                    setErrorMessages(err.message || "An error occurred during login.");
                }
                setSuccessMessage("");
            },
            newPasswordRequired: data => {
                console.log("newPasswordRequired:", data);
            }
        });
    };

    const confirmAccount = (event) => {
        event.preventDefault();

        const user = new CognitoUser({
            Username: email,
            Pool: Userpool
        });

        user.confirmRegistration(confirmationCode, true, (err, result) => {
            if (err) {
                console.error("Error confirming account:", err);
                setErrorMessages(err.message || "An error occurred during confirmation.");
            } else {
                setSuccessMessage("Account confirmed! You can now log in.");
                setShowConfirmationInput(false); // Hide confirmation input after success
                setErrorMessages("");
            }
        });
    };

    const logout = () => {
        localStorage.removeItem("user_id"); // Clear stored user_id
        setSuccessMessage("You have been logged out.");
        setEmail("");
        setPassword("");
    };
    

    return (
<div className='log-in-page'>
    {localStorage.getItem("user_id") ? (
        <div>
            <p>Welcome back!</p>
            <button className='log-out-btn' onClick={logout}>Log Out</button>
        </div>
    ) : (
        <motion.form  
            onSubmit={showConfirmationInput ? confirmAccount : onSubmit} // Conditional submit
            initial={{ opacity: 0, y: 50 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.9 }}
        >
            <h1>{showConfirmationInput ? "Confirm Your Account" : "Log In To Your Account!"}</h1>
            
            <input 
                type="email" 
                value={email} 
                onChange={(event) => setEmail(event.target.value)} 
                placeholder="Email"
                required
            />
            
            {!showConfirmationInput && (
                <input 
                    type="password" 
                    value={password} 
                    onChange={(event) => setPassword(event.target.value)} 
                    placeholder="Password"
                    required
                />
            )}

            {showConfirmationInput && (
                <input 
                    type="text" 
                    value={confirmationCode} 
                    onChange={(event) => setConfirmationCode(event.target.value)} 
                    placeholder="Enter confirmation code"
                    required
                />
            )}

            {errorMessages && <p className="error-message">{errorMessages}</p>}
            {successMessage && <p className="success-message">{successMessage}</p>}

            <Button submit="submit" text={showConfirmationInput ? 'Confirm' : 'Log In'} />
        </motion.form>
    )}
</div>
    );
}

export default LogIn;
