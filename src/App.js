import {BrowserRouter as Router, Routes, Route} from 'react-router-dom';
import Home from './pages/home/home';
import SignUp from './pages/signUp/SignUp';
import Navbar from './components/navbar/Navbar';
import  LogIn  from './pages/logIn/LogIn';
import AmplifyApp from './amplify/AmplifyApp';

function App() {

  return (
    <div className="App">
      <Router>
      <Navbar />
        <Routes>
          <Route path="/" element={<AmplifyApp/>} />
          <Route path="/sign-up" element={<SignUp />} />
          <Route path="/log-in" element={<LogIn />} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;
