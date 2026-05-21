const axios = require('axios');

// Equivalent to a basic GET request in Postman
axios.get('https://jsonplaceholder.typicode.com/posts/1')
  .then(response => {
    console.log("Status Code:", response.status);
    console.log("Post Title:", response.data.title);
  })
  .catch(error => console.error("Error fetching data:", error));