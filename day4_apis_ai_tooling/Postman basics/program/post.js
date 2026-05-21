const axios = require('axios');

// The payload data we configured in the Postman 'Body' tab
const newPost = {
  title: "Learning HTTP Methods",
  body: "Mapping Postman fields to executable application code.",
  userId: 1
};

// Sending a POST request
axios.post('https://jsonplaceholder.typicode.com/posts', newPost)
  .then(response => {
    console.log("Status Code:", response.status); // Expect 201 Created
    console.log("Created Record:", response.data);
  })
  .catch(error => console.error("Error creating record:", error));