import {BrowserRouter as Router, Routes, Route} from 'react-router-dom';
import Home from './pages/home/home';
import SignUp from './pages/signUp/SignUp';
import Navbar from './components/navbar/Navbar';


function App() {

  return (
    <div className="App">
              <Navbar />

      <Router>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/sign-up" element={<SignUp />} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;
