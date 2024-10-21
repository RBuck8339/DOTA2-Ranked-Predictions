// Buttons
const genDataBtn = document.getElementById('generateDataButton')
const predictBtn = document.getElementById('predictor')

// Frontend elements
const results = document.getElementById('results-table')
const dataTable = document.getElementById('data-table') // All rows in data table
const tbody = dataTable.querySelector('tbody'); // Get table body


// Adds the data to the table based on generated data
function renderData(data) {
    // Loop over each row
    Array.from(tbody.rows).forEach((dataRow, rowIdx) => {
        const cells = dataRow.querySelectorAll('td'); // Select only <td> elements

        // Loop over each cell in the row
        cells.forEach((cell, cellIdx) => {
            cell.textContent = data[rowIdx][cellIdx];
        });
    });
}

// Reads in data from the table to pass to the ML model
function readTable() {
    const storage = Array.from({ length: 20 }, () => Array(10));

    Array.from(tbody.rows).forEach((dataRow, rowIdx) => {
        const cells = dataRow.querySelectorAll('td'); // Select only <td> elements

        // Loop over each cell in the row
        cells.forEach((cell, cellIdx) => {

            val = cell.textContent.trim()
            val = parseFloat(val)

            // If there is a value here, store it
            if (!isNaN(val)) {
                storage[rowIdx][cellIdx] = val;
            } else {
                throw new Error('Missing value at row ${rowIdx + 1}, cell ${cellIdx + 1}')
            }
        });
    }); 
    return storage
}


// Displays the ML model results on the screen for the user
function renderResults(my_results) {
    // Change prediction result based on if radiant wins from binary 1/0 to True/False for readability
    if(my_results['prediction'] === 1) my_results['prediction'] = 'True'
    else my_results['prediction'] = 'False' 

    // Updates the results table based on the results received from the predict button
    results.innerHTML = `
        <table id="display-results">
            <tr> 
                <th>AUCROC</th>
                <th>Confidence Score</th>
                <th>Radiant Wins</th>
            </tr>
            <tr>
                <td>${my_results['AUCROC']}</td>
                <td>${my_results['confidence']}%</td>
                <td>${my_results['prediction']}</td>
            </tr>
        </table>
    `

    results.style.display = 'table'
}


// Grabs data from Python Flask connection to populate data table
genDataBtn.addEventListener('click', async() => {
    try {
        const response = await fetch('/get_data')

        // Parse the response
        const text = await response.text();
        const rawJson = JSON.parse(text);

        const data = rawJson.data // Get our data to display
        renderData(data)
    } catch (error) {
        results.innerHTML = 'Error fetching data'
        console.log('Error fetching data: ', error)
    }
})


// When the user presses the "PREDICT" button, use the model to predict
predictBtn.addEventListener('click', async () => {
    data = readTable()
    try{
        const prediction = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json', 
            },
            body: JSON.stringify(data)
        })
        const predictionJson = await prediction.json()
        renderResults(predictionJson)
    }
    catch (error){
        results.innerHTML = 'Failed to generate match prediction'
        results.style.display = 'flex'
    }
})