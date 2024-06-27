fetch('/api/fishes')
.then(response => response.json())
.then(data => {
    const tableBody = document.getElementById('fishes-table');
    data.forEach(fish => {
        const row = document.createElement('div.oneFish');
        row.innerHTML = `
            <div>${fish.common_name}</div>
            <div><img src="/static/assets/fish/${fish.img}" alt="${fish.common_name}"></div>
        `;
        tableBody.appendChild(row);
    });
})
.catch(error => console.error('Error fetching data:', error));