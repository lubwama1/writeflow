// NAVBAR
document.addEventListener("DOMContentLoaded", function() {
    const theme = localStorage.getItem("theme");
    const themeIcon = document.getElementById("theme-icon");
    if (theme === "dark") {
        document.body.classList.add("dark-mode");
        themeIcon.classList.remove("fa-moon");
        themeIcon.classList.add("fa-sun");
    }
});

document.getElementById("theme-toggle").addEventListener("click", () => {
    const themeIcon = document.getElementById("theme-icon");
    const isDarkMode = document.body.classList.toggle("dark-mode");
    if (isDarkMode) {
        localStorage.setItem("theme", "dark");
        themeIcon.classList.remove("fa-moon");
        themeIcon.classList.add("fa-sun");
    } else {
        localStorage.setItem("theme", "light");
        themeIcon.classList.remove("fa-sun");
        themeIcon.classList.add("fa-moon");
    }
});

// POST DETAIL PAGE
function toggleCommentForm() {
    const commentForm = document.getElementById("comment-form-container");
    commentForm.classList.toggle("hidden");
}

// AJAX to handle like/unlike functionality for post
function toggleLike() {
    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
    const postId = "{{ post.id }}";
    fetch("{% url 'sphere:post-detail' pk=post.id %}".replace("post.id", postId), {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken,
        },
        body: JSON.stringify({ action: "toggle_like" }),
    })
    .then((response) => response.json())
    .then((data) => {
        if (data.success) {
            const likeIcon = document.querySelector(`#like-form-${postId} i`);
            const likeCount = document.getElementById(`like-count-${postId}`);
            likeIcon.style.color = data.liked ? "#007bff" : "grey";
            likeCount.textContent = data.likes;
        }
    })
    .catch((error) => console.error("Error:", error));
}

// AJAX to handle comment like/unlike functionality
function toggleCommentLike(commentId) {
    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
    fetch("{% url 'sphere:post-detail' pk=post.id %}".replace("post.id", "{{ post.id }}"), {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken,
        },
        body: JSON.stringify({
            action: "toggle_comment_like",
            comment_id: commentId,
        }),
    })
    .then((response) => response.json())
    .then((data) => {
        if (data.success) {
            const likeIcon = document.querySelector(`#comment-like-form-${commentId} i`);
            const likeCount = document.getElementById(`comment-like-count-${commentId}`);
            likeIcon.style.color = data.liked ? "#007bff" : "grey";
            likeCount.textContent = data.likes;
        }
    })
    .catch((error) => console.error("Error:", error));
}

// SEARCH PAGE
document.getElementById('search-input').addEventListener('input', function () {
    let query = encodeURIComponent(this.value);
    // Handle dynamic search here, like filtering results or submitting
});

// CREATE POST PAGE
let postCount = 1;
const posts = document.querySelectorAll(".post-item");
const seeMoreBtn = document.getElementById("see-more-btn");
const seeLessBtn = document.getElementById("see-less-btn");

function updatePostsVisibility() {
    posts.forEach((post, index) => {
        post.style.display = (index < postCount) ? "block" : "none";
    });
    seeMoreBtn.style.display = (postCount < posts.length) ? "inline-block" : "none";
    seeLessBtn.style.display = (postCount > 1) ? "inline-block" : "none";
}

seeMoreBtn.addEventListener("click", function () {
    postCount += 1;
    updatePostsVisibility();
});

seeLessBtn.addEventListener("click", function () {
    postCount = 1;
    updatePostsVisibility();
});

updatePostsVisibility();
