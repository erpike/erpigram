import React, {useState, useEffect} from "react"
import "./Post.css"
import { Avatar, Button } from "@material-ui/core"

const BASE_URL = "http://localhost:8000/"

function Post({post, authToken, authTokenType, username, userId,}){
  const [imageUrl, setImageUrl] = useState("")
  const [comments, setComments] = useState([])
  const [newComment, setNewComment] = useState("")


  useEffect(
    () => {
      if (post.image_url_type === "absolute")
        setImageUrl(post.image_url)
      else
        setImageUrl(BASE_URL + post.image_url)
    },
    [post.image_url_type, post.image_url, post.comments]
  )

  useEffect(
    () => {
      setComments(post.comments)
    },
    [post.comments]
  )

  function handleDelete(event) {
    event?.preventDefault()

    const token = authTokenType + " " + authToken
    const requestOptions = {
      method: "DELETE",
      headers: new Headers({
        "Authorization": token,
      })
    }

    fetch(BASE_URL + "post/delete/" + post.id, requestOptions)
    .then(response => {
      if (response.ok) {
        window.location.reload()
        return response.json()
      }
      throw response
    })
    .catch(error=>{console.error(error)})


  }

  function postComment(event) {
    event?.preventDefault()
    const json_string = JSON.stringify({
      "user_id": userId,
      "text": newComment,
      "post_id": post.id,
    })

    const requestOptions = {
      method: "POST",
      headers: new Headers({
        "Authorization": authTokenType + " " + authToken,
        "Content-Type": "application/json",
      }),
      body: json_string,
    }

    fetch(BASE_URL + "comment", requestOptions)
    .then(response => {
      if(response.ok) {
        return response.json()
      }
      throw response
    })
    .then(() => {fetchComments()})
    .catch(error => {console.error(error)})
    .finally(() => {
      // clean form
      setNewComment("")
    })
  }

  const fetchComments = () => {
    fetch(BASE_URL + "comment/all/" + post.id)
    .then(response => {
      if(response.ok) {
        return response.json()
      }
      throw response
    })
    .then(data => {
      setComments(data)
    })
    .catch(error => {console.error(error)})
  }

  return (
    <div className="post">
      <div className="post_header">
        <Avatar alt="Catalin" src="" />
        <div className="post_header_info">
          <h3>{post.user.username}</h3>
            {
            (authToken && (username === post.user.username)) ?
              <Button className="post_delete" onClick={handleDelete}>Delete</Button>
            : null
          }
          
        </div>
      </div>
      <img className="post_image" src={imageUrl} alt="Post" />
      {/* <img className="post_image" src={(post.image_url_type === "absolute") ? post.image_url: BASE_URL + post.image_url} alt="Post" /> */}

      <h4 className="post_text">{post.caption}</h4>
      <div className="post_comments">
        {
          comments.map((comment) => (<p key={`comment-${comment.id}`}><strong>{comment.user.username}: </strong> {comment.text}</p>))
        }
      </div>
      {authToken && (
        <form className="post_comment_box">
          <input 
            className="post_input"
            type="text"
            placeholder="Add a comment"
            value={newComment}
            onChange={(e) => setNewComment(e.target.value)} 
          />
          <button 
            className="post_button"
            type="submit"
            disabled={!newComment}
            onClick={postComment}
          >Post</button>
        </form>
      )}

    </div>
  )
}

export default Post
