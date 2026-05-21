const axios = require('axios');

// Sending a DELETE request targeting post ID #1
axios.delete('https://jsonplaceholder.typicode.com/posts/1')
  .then(response => {
    console.log("Status Code:", response.status); // Expect 200 OK or 204 No Content
    console.log("Delete Confirmation:", response.data); // Usually empty or confirmation message
  })
  .catch(error => console.error("Error deleting record:", error));