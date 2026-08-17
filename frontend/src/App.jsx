import { useState } from 'react';
import Login from './Login';
import Register from './Register';
import Notes from './Notes';
import './index.css';

function App() {
  const [token, setToken] = useState(null);
  const [currentView, setCurrentView] = useState('login');

  return (
    <>
      {!token ? (
        currentView === 'login' ? (
          <Login setToken={setToken} setCurrentView={setCurrentView} />
        ) : (
          <Register setToken={setToken} setCurrentView={setCurrentView} />
        )
      ) : (
        <Notes token={token} setToken={setToken} />
      )}
    </>
  )
}

export default App;
