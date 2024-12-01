import {BrowserRouter as Router, Routes, Route} from 'react-router-dom';
import Home from './pages/home/home';
import Navbar from './components/navbar/Navbar';
import { Authenticator } from '@aws-amplify/ui-react';

import AmplifyApp from './AmplifyApp';

function App() {
  return (
    <div className="App">
      <Router>
        <Authenticator>
          {({ signOut, user }) => (
            <>
              <Navbar signOut={signOut} />
              <Routes>
                <Route path="/" element={<AmplifyApp/>} />
                <Route path="/home" element={<Home />} />
              </Routes>
            </>
          )}
        </Authenticator>
      </Router>
    </div>
  );
}

export default App;