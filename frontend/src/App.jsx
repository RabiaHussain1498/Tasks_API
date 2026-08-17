import { useState } from 'react';
import Login from './Login';
import Notes from './Notes';
import './index.css';

function App() {
  const [token, setToken] = useState(null);

  return (
    <>
      {!token ? (
        <Login setToken={setToken} />
      ) : (
        <Notes token={token} setToken={setToken} />
      )}
    </>
  )
}

export default App;
