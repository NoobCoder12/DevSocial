// Likes
const hearts = document.querySelectorAll('.fa-solid.fa-heart')

hearts.forEach(el => {
  el.addEventListener('click', () => {
    const slug = el.dataset.slug;

    const postContainer = el.closest('.post');

    const likesCounter = postContainer.querySelector('.likes-count');

    fetch(`/interactions/post/${slug}/like/`, {
      method: "POST",
      headers: {
        'X-CSRFToken': getCookie('csrftoken'),
        'Content-Type': 'application/json',
      }
    })
    .then(res => res.json())
    .then(data => {
      el.classList.toggle('liked', data.liked); // Class on if data.liked is true

      likesCounter.textContent = data.likes_count;
    })
    .catch(err => console.error(err));
    });
});

// Comments
const comments = document.querySelectorAll(".fa-solid.fa-comment")

comments.forEach((comment) => {
  comment.addEventListener('click', (event) => {
    comment.classList.toggle("commenting")

    const postSlug = event.currentTarget.dataset.postSlug;
    const box = document.getElementById(`comment-box-${postSlug}`);

    box.classList.toggle("comment-ready");
  })
})

function addComment(slug) {
  const input = document.getElementById(`input-${slug}`) 
  const body = input.value.trim()

  if (!body) return;

  fetch(`/interactions/post/${slug}/comment/`, {
    method: "POST",
    headers: {
      'X-CSRFToken': getCookie('csrftoken'),
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ "body": body })
  })
  .then((res) => res.json())
  .then(data => {
    if (data.status === "success") {
      const list = document.getElementById(`comment-list-${slug}`);
      
      // Inserting HTML at the div start / CAREFULLY WITH INJECTIONS
      list.insertAdjacentHTML('afterbegin', data.html);

      input.value = "";
      
      // Delete message "No comments yet"
      const emptyMsg = list.querySelector('.no-comments');
      if (emptyMsg) emptyMsg.remove();

      // Comment counter update after adding comment
      const postContainer = list.closest(".post")
      const commentCounter = postContainer.querySelector(".comments-count")

      if (commentCounter) {
        // Get the value from html element
        let count = parseInt(commentCounter.textContent);
        commentCounter.textContent = count + 1;
      }

    }
  }) 
  .catch(err => console.error(err.message))
}