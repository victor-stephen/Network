function editPost(e) {
    // Hide the edit and like button to save button
    document.querySelector(`#editbutton${e}`).style.display = "none";
    document.querySelector(`#likebutton${e}`).style.display = "none";
    
    // Get the post to be edited
    var postdiv = document.querySelector(`#post${e}`);
    var postContent = postdiv.innerHTML;

    // Hide the post
    postdiv.style.display = "none";

    // Show the form to edit the post
    document.querySelector(`#editPost${e}`).style.display = "block";

    // Prefill the form with the post to be edited
    document.querySelector(`#prefillpost${e}`).innerHTML = postContent;

    // Listen for submission of form
    document.querySelector(`#editPost${e}`).addEventListener("onsubmit", () => submitPost(e));
    
};

function submitPost(e) {
    // Get content of form
    console.log(e);

    // Stop for from submitting
    return false
};
