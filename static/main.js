let chart;  // Global variable to store the chart instance

document.getElementById('search-form').addEventListener('submit', function (event) {
    event.preventDefault();
    
    let query = document.getElementById('query').value;
    let resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = '';
    document.getElementById('similarity-chart').style.display = 'none';

    fetch('/search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
            'query': query
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        displayResults(data);
        displayChart(data);
    });
});

function displayResults(data) {
    let resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = '<h2>Results</h2>';
    for (let i = 0; i < data.documents.length; i++) {
        let docDiv = document.createElement('div');
        docDiv.innerHTML = `<strong>Document ${data.indices[i]}</strong><p>${data.documents[i]}</p><br><strong>Similarity: ${data.similarities[i].toFixed(4)}</strong>`;
        resultsDiv.appendChild(docDiv);
    }
}

function displayChart(data) {

    if (chart) {
        chart.destroy();
    }

    let ctx = document.getElementById('similarity-chart').getContext('2d');
    document.getElementById('similarity-chart').style.display = 'block';

    chart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.indices.map(i => 'Doc ' + i),
            datasets: [{
                label: 'Cosine Similarity',
                data: data.similarities,
                backgroundColor: 'rgba(0, 123, 255, 0.6)'
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true,
                        suggestedMax: 1
                    }
                }]
            }
        }
    });
}
