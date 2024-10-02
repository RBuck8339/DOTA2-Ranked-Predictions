// Buttons
const genDataBtn = document.getElementById('generateDataButton')
const predictBtn = document.getElementById('predictor')
const results = document.getElementById('results-table')
const dataTable = document.getElementById('data-table')


// Adds the data to the table based on generated data
function renderData(my_data) {
    dataTable.innerHTML = `
    
    `
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
        const data = await fetch('/get_data')
        renderData(data)
    }
    catch{
        results.innerHTML = 'Error fetching data'
    }
})


// When the user presses the "PREDICT" button, use the model to predict
predictBtn.addEventListener('click', async () => {
    try{
        const prediction = await fetch('/predict')
        renderResults(prediction)
    }
    catch (error){
        results.innerHTML = 'Failed to generate match prediction'
        results.style.display = 'flex'
    }
})