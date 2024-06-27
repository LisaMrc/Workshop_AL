fetch('/api/fishes')
.then(response => response.json())
.then(data => {
    const tableBody = document.getElementById('fishes-table');
    data.forEach(fish => {
        const row = document.createElement('div');
        row.className = "oneFish";
        row.innerHTML = `
            <div><img src="/static/assets/fish/${fish.img}" alt="${fish.common_name}"></div>
            <div>${fish.common_name}</div>
            <div class="card-overlay">
            <h2>${fish.scientific_name}</h2>
                <p>${fish.family} family</p>
                <p>Size: ${fish.average_size} m</p>
            </div>
        `;
        tableBody.appendChild(row);
    });
})
.catch(error => console.error('Error fetching data:', error));