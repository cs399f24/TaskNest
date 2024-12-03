import { useState } from 'react';
import styles from './Navbar.module.css';
import { useNavigate } from 'react-router-dom';

function Navbar({ signOut }) {
    const [isActive, setIsActive] = useState(false);
    const navigate = useNavigate();

    const toggleActiveClass = () => {
        setIsActive(!isActive);
    };

    const handleSignOut = () => {
        localStorage.removeItem("user_id");
        signOut();
        navigate('/');
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
                        <li>
                            <button onClick={handleSignOut} className={styles.navLink}>Sign Out</button>
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