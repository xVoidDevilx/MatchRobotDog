// Import the necessary server libs
const express = require('express')
const path = require('path')

const app = express();

//serve static files from public dir
app.use(express.static(path.join(__dirname, 'public')))

// Define a route to the html file
app.get('/', (req, res) => 
{
    res.sendFile(path.join(__dirname, 'public', 'dashboard.html'))
})

const PORT = process.env.PORT || 5000

app.listen(PORT, () =>
{
    console.log(`Server running on port ${PORT}`)
})