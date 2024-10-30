import { useState } from 'react';
import styles from './Navbar.module.css';
import logo from '../../assets/logo.png'
import {motion} from 'framer-motion'
import { useNavigate } from 'react-router-dom'; // Import useNavigate


function Navbar() {


    const [isActive, setIsActive] = useState(false);


    const toggleActiveClass = () => {
        setIsActive(!isActive);
    };
    {/**

         const handleSignUpClick = () => {
        navigate('/sign-up'); // Navigate to the Sign Up route
        setIsActive(false); // Optionally close the menu after clicking
    };

        const navigate = useNavigate(); // Initialize useNavigate


         */}

  

    return (
        <div className={styles.main}>
            <header className={styles.navbarHeader}>
                <nav className={styles.navbar}>
                    <div className={styles.logo}>
                        <h3>tasknest</h3>
                    </div>

                    <ul className={`${styles.navMenu} ${isActive ? styles.active : 'navMenuDefault'}`}>
                        <li>
                            <a href='/' className={styles.navLink}>Login</a>
                        </li>
                        <li>
                        <a 
                                href="#" // Change href to "#" to prevent default link behavior
                                id='sign-up' 
                                className={styles.navLink}
                                // Use handleSignUpClick
                            >
                                Sign Up
                            </a>
                        </li>

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