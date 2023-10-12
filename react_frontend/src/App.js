import './App.css';
import {useEffect, useState} from 'react';
import Post from "./Post/Post";
import ImageUpload from "./ImageUpload"
import { Button, Modal, makeStyles, Input } from '@material-ui/core';

const BASE_URL = "http://localhost:8000/"

function getModalStyle() {
  const top = 50
  const left = 50
  return {
    top: `${top}%`,
    left: `${left}%`,
    transform: `translate(-${top}%, -${left}%)`,
  }
}

const useStyles = makeStyles((theme) => ({
  // TODO: read docs of material design library
  paper: {
    backgroundColor: theme.palette.background.paper,
    position: "absolute",
    width: 400,
    border: "2px solid #000",
    boxShadow: theme.shadows[5],
    padding: theme.spacing(2, 4, 3),
  }
}))

function App() {
  const classes = useStyles()

  const [posts, setPosts] = useState([]);
  const [OpenSignIn, setOpenSignIn] = useState(false)
  const [OpenSignUp, setOpenSignUp] = useState(false)
  const [modalStyle, setModalStyle] = useState(getModalStyle)
  
  const [username, setUsername] = useState("")
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [authToken, setAuthToken] = useState(null)
  const [authTokenType, setAuthTokenType] = useState(null)
  const [userId, setUserId] = useState(null)

  useEffect(() => {
    function refreshAccessToken() {
      if (!window.localStorage.getItem("refreshToken")) {
        return
      }

    const token_data = window.localStorage.getItem("refreshToken")
    
    const json_string = JSON.stringify({
      token: token_data
    })

    const requestOptions = {
      method: "POST",
      headers: {"Content-Type": "application/json"}, 
      body: json_string,
    }

      fetch(BASE_URL + "refresh", requestOptions)
      .then(response => {
        if (response.ok) {
          return response.json()
        }
        throw response
      })
      .then((data) => {
        setAuthToken(data.access_token)

      })
      .catch(error => {
        console.error(error)
        window.localStorage.removeItem("refreshToken")
      })
    }

    refreshAccessToken()
    setInterval(refreshAccessToken, 1000 * 60 * 29)
    
  }, [])

  useEffect(() => {
    setAuthToken(window.localStorage.getItem("authToken"))
    setAuthTokenType(window.localStorage.getItem("authTokenType"))
    setUsername(window.localStorage.getItem("username"))
    setUserId(window.localStorage.getItem("userId"))
  }, [])

  useEffect(() => {
    authToken ? window.localStorage.setItem("authToken", authToken) : window.localStorage.removeItem("authToken")
    authTokenType ? window.localStorage.setItem("authTokenType", authTokenType) : window.localStorage.removeItem("authTokenType")
    userId ? window.localStorage.setItem("userId", userId) : window.localStorage.removeItem("userId")
    username ? window.localStorage.setItem("username", username) : window.localStorage.removeItem("username")
  }, [authToken, authTokenType, userId])

  useEffect(() => {
    fetch(BASE_URL + "post")
    .then(response => {
      if (response.ok) {
        return response.json()
      }
      throw response
    })
    .then(data => {
      const result = data.sort((a, b) => {
        /*
        sort by timestamp
        const t_a = a.timestamp.split(/[-T:]/)
        const t_b = b.timestamp.split(/[-T:]/)
        const d_a = new Date(Date.UTC(t_a[0], t_a[1]-1, t_a[2], t_a[3], t_a[4], t_a[5]))
        const d_b = new Date(Date.UTC(t_b[0], t_b[1]-1, t_b[2], t_b[3], t_b[4], t_b[5]))
        return d_b - d_a
        */
        return b.id - a.id        
      })
      return result
    })
    .then(data => {
      setPosts(data)
    })
    .catch(error => {
      console.error(error); 
    })
  }, [])
  
  function signIn(event) {
    if (event) event.preventDefault()
    let formData = new FormData()
    formData.append("username", username)
    formData.append("password", password)

    const requestOptions = {
      method: "POST",
      body: formData,
    }

    fetch(BASE_URL + "login", requestOptions)
    .then(response => {
      if (response.ok) {
        return response.json()
      }
      throw response
    })
    .then(data => {
      setAuthToken(data.access_token)
      setAuthTokenType(data.token_type)
      setUserId(data.user_id)
      setUsername(data.username)
      setPassword("")
      window.localStorage.setItem("refreshToken", data.refresh_token)
    })
    .catch(error => {
      setUsername(null)
      setPassword(null)
      console.error(error)
    })

    setOpenSignIn(false)

  }

  function signOut() {
    setAuthToken(null)
    setAuthTokenType(null)
    setUserId(null)
    setUsername("")
  }

  const signUp = (event) => {
    event.preventDefault()

    const json_string = JSON.stringify({
      username: username,
      email: email,
      password: password,
    })

    const requestOptions = {
      method: "POST",
      headers: {"Content-Type": "application/json"}, 
      body: json_string,
    }

    fetch(BASE_URL + "user", requestOptions)
    .then(response => {
      if (response.ok) {
        return response.json()
      }
      return response.json().then(data => { throw new Error(data.detail) })
    })
    .then((data) => {
      signIn()
    })
    .catch(error => {console.error(error)})
    setOpenSignUp(false)

  }

  return (
    <div className="app">
      <Modal 
        open={OpenSignIn}
        onClose={() => setOpenSignIn(false)}
      >
        <div style={modalStyle} className={classes.paper}>
          <form className="app_sign_in">
            <center>
              <img className="app_header_image" src="/erpigram.png" alt="erpigram" />
            </center>

            <Input placeholder="username" type="text" value={username || ""} onChange={e => setUsername(e.target.value)} />
            <Input placeholder="password" type="password" value={password} onChange={e => setPassword(e.target.value)} />
            <Button type="submit" onClick={signIn}>Login</Button>
          </form>
        </div>
      </Modal>

      <Modal 
        open={OpenSignUp}
        onClose={() => setOpenSignUp(false)}
      >
        <div style={modalStyle} className={classes.paper}>
          <form className="app_sign_in">
            <center>
              <img className="app_header_image" src="/erpigram.png" alt="erpigram" />
            </center>

            <Input placeholder="username" type="text" value={username || ""} onChange={e => setUsername(e.target.value)} />
            <Input placeholder="email" type="text" value={email} onChange={e => setEmail(e.target.value)} />
            <Input placeholder="password" type="password" value={password} onChange={e => setPassword(e.target.value)} />
            <Button type="submit" onClick={signUp}>Sign Up</Button>
          </form>
        </div>
      </Modal>

      <div className="app_header">
        <img className="app_header_image" src="/erpigram.png" alt="erpigram" />
        
        {authToken ? (
          <Button onClick={signOut} >Logout</Button>
        ) : (
          <div>
            <Button onClick={() => setOpenSignIn(true)}>Sign In</Button>
            <Button onClick={() => setOpenSignUp(true)}>Sign Up</Button>
          </div>
        )}
      </div>

      <div className="app_posts">
        {
          posts.map(
            (post) => (
              <Post
                post={post}
                key={`post-${post.id}`}
                authToken={authToken}
                authTokenType={authTokenType}
                userId={userId}
                username={username}
              />
            )
          )
        }
      </div>

      {
        authToken ? (
          <ImageUpload authToken={authToken} authTokenType={authTokenType} userId={userId} />
        ) : (
          <h3>You need to login to upload.</h3>
        )
      }
    </div>
  )
}

export default App;
