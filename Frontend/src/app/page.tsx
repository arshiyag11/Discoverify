"use client"
import { Black_Han_Sans } from "next/font/google";
import {useState} from "react";

export default function Home() {
  const [token, setToken] = useState('');
  const [playlistID, setPlaylistID] = useState('');
  const [loggedIn, setLoggedIn] = useState(false);

  const handleShuffle = (e: React.FormEvent) => {
    e.preventDefault(); // Prevent default form submission

    const apiUrlPost = 'http://localhost:5000/api/shuffle';
    const postData = { ID: playlistID, Token: token };
    const requestOptions = {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(postData),
    };

    fetch(apiUrlPost, requestOptions)
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => { 
        return console.log(data);
      })
      .catch(error => alert('Error: ' + error.message));
  };


  // const handleShuffle = (e: React.FormEvent) => {
  //   // Make post request to send playlist id to backend
  //   const apiUrlPost = 'http://localhost:5000/api/shuffle';
    
  //   const postData = { ID: playlistID, Token: token };
  //   const requestOptions = {
  //     method: 'POST',
  //     headers: {
  //       'Content-Type': 'application/json',
  //     },
  //     body: JSON.stringify(postData),
  //   };

  //   console.log('Request Data:', JSON.stringify(postData));

  //   fetch(apiUrlPost, requestOptions)
  //     .then(response => {
  //       if (!response.ok) {
  //         throw new Error(`HTTP error! Status: ${response.status}`);
  //       }
  //       const contentType = response.headers.get('Content-Type');
  //       if (!contentType || !contentType.includes('application/json')) {
  //         throw new Error('Invalid content type in response');
  //       }
  //       return response.json();
  //     })
  //     .then(data => console.log(data))
  //     .catch(error => alert('Error: ' + error.message));

    // // Make post request to send playlist id to backend
    // const apiUrlPost = 'http://localhost:5000/api/shuffle';
    // const postData = {ID : playlistID};
    // const requestOptions = {
    //   method: 'POST',
    //   headers: {
    //     'Content-Type' : 'application/json',
    //   },
    //   body: JSON.stringify(postData),
    // };
    // fetch(apiUrlPost, requestOptions)
    // .then(response => {
    //   if (!response.ok) {
    //     throw new Error(`HTTP error! Status: ${response.status}`);
    //   }
    //   return response.json();
    // })
    // .then(data => alert(data))
    // .catch(error => alert('Error: ' + error));
  // };

  const handleLogin = () => {
    const apiUrl = 'http://localhost:5000/api/gentoken';
    fetch(apiUrl)
    .then(response => response.json())
    .then(data => {
      setToken(data.token);
      setLoggedIn(true);
    })
    .catch(error => {
      // Handle errors
      console.error('Error:', error);
      alert('Error: ' + error.message);
    });
    // Perform login logic (e.g., send credentials to server)
  };

  const neonTextStyle: React.CSSProperties = {
    fontFamily: 'Arial, sans-serif', 
    color: 'transparent',
    textTransform: 'uppercase',
    fontSize: '4em',
    letterSpacing: '5px',
    background: 'linear-gradient(90deg, #00ff00, #00ff00)', // Change the color to white
    WebkitBackgroundClip: 'text',
    backgroundClip: 'text',
    animation: 'neon 0.5s ease-in-out infinite',
    textShadow: '0 0 10px rgba(0, 255, 0, 0.9), 0 0 20px rgba(0, 255, 0, 0.9), 0 0 30px rgba(0, 255, 0, 0.9)',
  };

  const purpleTextStyle: React.CSSProperties = {
    fontFamily: 'Arial, sans-serif', 
    color: 'transparent',
    textTransform: 'uppercase',
    fontSize: '4em',
    letterSpacing: '5px',
    background: 'linear-gradient(45deg, #4b0082, #9400d3)', 
    WebkitBackgroundClip: 'text',
    backgroundClip: 'text',
    animation: 'neon 0.5s ease-in-out infinite',
    textShadow: '0 0 10px rgba(208, 0, 255, 0.9), 0 0 20px rgba(208, 0, 255, 0.9), 0 0 30px rgba(208, 0, 255, 0.9)',
  };

  const formStyle: React.CSSProperties = {
    backgroundColor: 'rgb(0 0 0)', 
    padding: '20px',
    borderRadius: '10px',
  };

  const spotifyButtonStyle: React.CSSProperties = {
    fontFamily: 'Arial, sans-serif',
    fontSize: '1em',
    letterSpacing: '2px',
    padding: '10px 20px',
    color: 'rgba(0, 255, 0, 0.9)', // Set text color to a visible color
    backgroundColor: 'transparent', // Set the background color to transparent
    border: '2px solid transparent', // Set a transparent border
    borderRadius: '5px',
    position: 'relative',
    overflow: 'hidden',
    cursor: 'pointer',
    transition: 'background-color 0.3s, border-color 0.3s, color 0.3s',
    borderColor: 'rgba(0, 255, 0, 0.9)', // Purple glow color
    boxShadow: '0 0 10px rgba(0, 255, 0, 0.9), 0 0 20px rgba(0, 255, 0, 0.9), 0 0 30px rgba(0, 255, 0, 0.9)',
  };  
  
  const purpleButtonStyle: React.CSSProperties = {
    fontFamily: 'Arial, sans-serif',
    fontSize: '1em',
    letterSpacing: '2px',
    padding: '10px 20px',
    color: 'rgba(208, 0, 255, 0.9)', // Set text color to a visible color
    backgroundColor: 'transparent', // Set the background color to transparent
    border: '2px solid transparent', // Set a transparent border
    borderRadius: '5px',
    position: 'relative',
    overflow: 'hidden',
    cursor: 'pointer',
    transition: 'background-color 0.3s, border-color 0.3s, color 0.3s',
    borderColor: 'rgba(208, 0, 255, 0.9)', // Purple glow color
    boxShadow: '0 0 10px rgba(208, 0, 255, 0.9), 0 0 20px rgba(208, 0, 255, 0.9), 0 0 30px rgba(208, 0, 255, 0.9)',
  };
  
  return (
      (
          <div className="min-h-screen flex flex-col items-center bg-cover justify-center" style={{ 
              backgroundRepeat: 'no-repeat', backgroundColor: 'black', minHeight: '100vh', backgroundPosition: 'center' }}>
            <div className="text-center mb-4">
              <h1 style={neonTextStyle}>Discoverify</h1>
            </div>
            <div className="text-center mb-4">
                <button type="submit" className= {`btn btn-wide ${loggedIn ? "" : "btn-disable"}`} style={spotifyButtonStyle} onClick={handleLogin}>
                {loggedIn ? 'Welcome' : 'Log in'}
                </button>
            </div>
            <div className="w-2/5 h-1/5 flex items-center justify-center p-4 bg-base-100 shadow-xl rounded-lg">
              <form onSubmit={handleShuffle} style={formStyle} className="w-full text-center">
                <div className="mb-4">
                  <input
                      type="text"
                      placeholder="Enter Playlist Link"
                      value={playlistID}
                      onChange={e => setPlaylistID(e.target.value)}
                      className="input input-bordered w-full max-w-xs mb-2"
                      required
                  />
                </div>
                <button type="submit" className= {`btn btn-wide ${loggedIn ? "" : "btn-disable"}`} style={spotifyButtonStyle}>
                  Shuffle
                </button>
              </form>
            </div>
          </div>
    )
  );
}