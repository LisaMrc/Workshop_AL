fetch('/api/fish')
.then(response => response.json())
.then(data => {
    console.log(data);
})
.catch(error => console.error('Error fetching data:', error));