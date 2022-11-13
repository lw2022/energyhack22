let stackedVis;

let csv = "data/ampData.csv";

// read csv data from data folder
d3.csv("data/ampData.csv", function(data){
    console.log(data);
    createVis(data);
});

function createVis(data){
    stackedVis = new StackedVis("#stackedVis", data);
}