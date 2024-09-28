// Buttons
const genDataBtn = document.getElementById('generateDataButton')
const predictBtn = document.getElementById('predictor')
const results = document.getElementById('results')

function renderResults(){
    results.innerHTML = `
        <table id="display-results">
        
        </table>
    `
}

// Grabs data from Python Flask connection to populate data table
genDataBtn.addEventListener('click', function() {
    
})


// When the user presses the "PREDICT" button, use the model to predict
predictBtn.addEventListener('click', function() {

})