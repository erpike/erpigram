import './App.css';
import {useEffect, useState} from 'react';

const BASE_URL = "http://localhost:8000/"

function App() {
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    fetch(BASE_URL + "post")
      .then(response => {
        var json = response.json();
        if (response.ok) {
          return json;
        }
        throw response;
      })
      .then(data => {
        setPosts(data);
      })
      .catch(error => {
        console.log(error);
        alert(error); 
      })
  }, [])
  
  return (
    "Hello world!"
  );
}

export default App;
