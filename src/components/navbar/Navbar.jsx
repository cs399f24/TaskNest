import { useState,useEffect } from 'react';
import styles from './Navbar.module.css';
import logo from '../../assets/logo.png'
import { motion } from 'framer-motion'
import { useNavigate } from 'react-router-dom';

function Navbar() {

    const [isActive, setIsActive] = useState(false);
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const navigate = useNavigate();

    const toggleActiveClass = () => {
        setIsActive(!isActive);
    };

    useEffect(() => {
        const interval = setInterval(() => {
            setIsLoggedIn(!!localStorage.getItem("user_id"));
        }, 1000);

        return () => clearInterval(interval); // Cleanup interval on component unmount
    }, []);

    const handleLogout = () => {
        localStorage.removeItem("user_id"); // Clear user_id from localStorage
        localStorage.removeItem("accessToken"); // Clear accessToken from localStorage
        localStorage.removeItem("idToken"); // Clear idToken from localStorage
        setIsLoggedIn(false); // Update isLoggedIn state
        navigate('/log-in'); // Redirect to the home page
    };

    return (
        <div className={styles.main}>
            <header className={styles.navbarHeader}>
                <nav className={styles.navbar}>
                    <div className={styles.logo}>
                        <a href="/">
                            <h3>tasknest</h3>
                        </a>
                    </div>

                    <ul className={`${styles.navMenu} ${isActive ? styles.active : 'navMenuDefault'}`}>
                    {isLoggedIn ? (
                            // Show Logout if user is logged in
                            <li>
                                <button  onClick={handleLogout} className={styles.navLink}>Logout</button>
                            </li>
                        ) : (
                            // Show Login and Sign Up if user is not logged in
                            <>
                                <li>
                                    <a href='/log-in' className={styles.navLink}>Login</a>
                                </li>
                                <li>
                                    <a href="/sign-up" className={styles.navLink}>Sign Up</a>
                                </li>
                            </>
                        )}
                    </ul>
                    <div
                        className={`${styles.hamburger} ${isActive ? styles.active : ''}`}
                        onClick={toggleActiveClass}
                    >
                        <span className={styles.bar}></span>
                        <span className={styles.bar}></span>
                        <span className={styles.bar}></span>
                    </div>
                </nav>
            </header>
        </div>
    );
}

export default Navbar;