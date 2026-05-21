const axios = require('axios');

// The updated data block
const updatedPost = {
  id: 1,
  title: "This Title Has Been Updated",
  body: "The content body has been replaced completely.",
  userId: 1
};

// Sending a PUT request targeting specific post ID #1
axios.put('https://jsonplaceholder.typicode.com/posts/1', updatedPost)
  .then(response => {
    console.log("Status Code:", response.status); // Expect 200 OK
    console.log("Updated Record:", response.data);
  })
  .catch(error => console.error("Error updating record:", error));