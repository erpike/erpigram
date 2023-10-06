import React, {useState} from "react"
import { Button } from "@material-ui/core"
import "./ImageUpload.css"

const BASE_URL = "http://localhost:8000/"

function ImageUpload({authToken, authTokenType, userId}) {
    const [caption, setCaption] = useState("")
    const [image, setImage] = useState(null)

    const formData = new FormData()
    formData.append("image", image)

    function handleChange(event) {
        if (event.target.files[0]) {
            setImage(event.target.files[0])
        }
    }

    function createPost(imageUrl) {

        const json_string = JSON.stringify({
            "image_url": imageUrl,
            "image_url_type": "relative",
            "caption": caption,
            "user_id": userId,
        })
        const requestOptions = {
            method: "POST",
            headers: new Headers({
                "Authorization": authTokenType + " " + authToken,
                "Content-Type": "application/json",
            }),
            body: json_string,
        }

        fetch(BASE_URL + "post", requestOptions)
        .then(response => {
            if (response.ok) {
                return response.json()
            }
            throw response
        })
        .then((data) => {
            window.location.reload()
            window.scrollTo(0, 0)
        })
        .catch(error => {console.error("ERROR", error)})

    }

    const handleUpload = (event) => {
        if (event) {
            event.preventDefault()
        }  // event?.preventDefault()
        
        const requestOptions = {
            method: "POST",
            headers: new Headers({
                "Authorization": authTokenType + " " + authToken
            }),
            body: formData,
        }

        fetch(BASE_URL + "post/image", requestOptions)
        .then(response => {
            if (response.ok) {
                return response.json()
            }
            throw response
        })
        .then(data => {
            createPost(data.filename)
        })
        .catch(error => {console.error("ERROR", error)})
        .finally(() => {
            // reason: reset UI
            setImage(null)
            setCaption("")
            document.getElementById("file_input").value = null
        })
    }

    return (
        <div className="image_upload">
            <input
                type="text"
                placeholder="Enter a caption"
                onChange={(event) => {setCaption(event.target.value)}}
                value={caption} 
            />
            <input type="file" id="file_input" onChange={handleChange}/>
            <Button className="image_upload_button" onClick={handleUpload} >Upload</Button>
        </div>
    )
}

export default ImageUpload