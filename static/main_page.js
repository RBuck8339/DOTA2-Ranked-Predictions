// Buttons
const genDataBtn = document.getElementById('generateDataButton')
const predictBtn = document.getElementById('predictor')
const results = document.getElementById('results-table')
const dataTable = document.querySelectorAll('#data-table tbody tr')  // All rows in data table


// Needs testing
// Adds the data to the table based on generated data
function renderData(my_data) {
    // Loop over each row
    my_data.forEach((dataRow, row_idx) => {
        const row = dataTable[row_idx + 1]
        const curr_cells = row.querySelectorAll('td') // Get the current row's cells

        // Loop over the cells
        curr_cells.forEach((cell, cell_idx) =>{
            cell.textContent = dataRow[cell_idx] 
        })
    })
}


function readTable(){
    let storage = [[]] // Tmp
    try{
        // Loops over the data and stores it
        dataTable.forEach((row, row_idx) => {
            const curr_cells = row.querySelectorAll('td')

            curr_cells.forEach((cell, cell_idx) =>{
                val = td.textContent // Need to figure out how to make floating point nums instead of strings

                // Error handlers
                if(val < 0) throw "There should be no negative values in the data"
                else if(val == null) throw "All data fields must be filled"

                storage[row_idx][cell_idx] = val // Put into data table
            })
        })
    }
    catch(error){
        console.log(error)
    }
}


// Displays the ML model results on the screen for the user
function renderResults(my_results){

    // Updates the results table based on the results received from the predict button
    results.innerHTML = `
        <table id="display-results">
        <th></th>
        </table>
    `
    results.style.display = 'table'
}


// Grabs data from Python Flask connection to populate data table
genDataBtn.addEventListener('click', async () => {
    try{
        const response = await fetch('/get_data')
        const data = await response.json()
        console.log(JSON.stringify(data))
        data = data['data']
        renderData(data)
    }
    catch (error) {
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
                'Content-Type:': 'application/json',
            },
            body: JSON.stringify(data)
        })
        renderResults(prediction)
    }
    catch (error){
        results.innerHTML = 'Failed to generate match prediction'
        results.style.display = 'flex'
    }
})