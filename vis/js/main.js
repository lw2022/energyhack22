let stackedVis;

let csv = "data.csv";

// read csv data from data folder
d3.csv(csv).then(csvData => {
    console.log(csvData)
    createVis(csvData)
});

function createVis(data){
    stackedVis = new StackedVis("#stackedVis", data);
}