function editPost(e) {
    // Hide the edit and like button to save button
    document.querySelector(`#editbutton${e}`).style.display = "none";
    document.querySelector(`#likebutton${e}`).style.display = "none";
    
    // Get the post to be edited
    var postdiv = document.querySelector(`#post${e}`);
    var postContent = postdiv.innerHTML;

    // Clear post
    postdiv.innerHTML = "";

    // Hide the post
    postdiv.style.display = "none";

    // Show the form to edit the post
    document.querySelector(`#editPost${e}`).style.display = "block";

    // Prefill the form with the post to be edited
    document.querySelector(`#prefillpost${e}`).innerHTML = postContent;

    // Listen for submission of form
    document.querySelector(`#editPost${e}`).addEventListener("submit", (event) => {
        event.preventDefault();
        submitPost(e);
    });
    
};

function submitPost(e) {
    // Get the post from form
    const post = document.querySelector(`#prefillpost${e}`).value

    fetch(`/editPost/${e}`, {
        method: "POST",
        headers: {"Content-type": "application/json"},
        body: JSON.stringify({
            post: post
        }),
    })
    .then((response) => response.json())
    .then((data) => {
        console.log("Success:", data);
        var postdiv = document.querySelector(`#post${e}`)
        postdiv.innerHTML = data.post
        
        // Hide form and clear textarea
        document.querySelector(`#editPost${e}`).style.display = "none";
        document.querySelector(`#prefillpost${e}`).innerHTML = "";

        // Display new post
        postdiv.style.display = "block";
        // Hide the edit and like button to save button
        document.querySelector(`#editbutton${e}`).style.display = "inline-block";
        document.querySelector(`#likebutton${e}`).style.display = "inline-block";
    })
};

