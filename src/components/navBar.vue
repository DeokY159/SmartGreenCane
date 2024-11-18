<template>
    <div class="row">
      <!-- Navbar -->
      <nav class="component-navbar">
        <div class="col-8 title">
            <img src ="../assets/greencane.png" alt = "Logo" style="width: 50px; margin-left: 20px;">
            <p>Green cane management application</p>
        </div>
        <ul>
          <li><a href="https://github.com/DeokY159/2024_OpenSource_GreenCane.git" target="_blank">GitHub</a></li>
        </ul>
      </nav>
      <!-- The rest of your component's content -->
    </div>
</template>

<style scoped>
  .component-navbar {
  background-color: #81BE83; /* Set the background color for the navbar */
  padding: 10px; /* Add padding to provide spacing */
}

.component-navbar .title {
    display: flex;
    align-items: center;
    color: #fff; /* White text color */
    font-size: 25px; /* Larger font size */
    font-weight: bold; /* Bold font weight */
}

.component-navbar .title p {
  margin : 0;
  margin-left: 15px;
}

.component-navbar ul {
  float: right; /* Float the list to the right */
  align-items: center; /* Center-align list items */
  list-style-type: none; /* Remove the bullet points for the list */
  display: inline-box;
  padding: 15px;
  margin: 0px;
}

.component-navbar li {
  display: inline; /* Display list items horizontally */
  text-align: center; /* Center-align list items */
  margin-left: 20px; /* Add space between list items */
  margin-right: 20px; /* Add space between list items */
}

.component-navbar a {
  text-decoration: none; /* Remove underlines from links */
  color: #fff; /* Set the text color to white */
  font-weight: bold; /* Make the text bold */
  font-size: 16px; /* Adjust the font size */
}

.component-navbar a:hover {
  text-decoration: underline; /* Add underline on hover */
}

  </style>
  