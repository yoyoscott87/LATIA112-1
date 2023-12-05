let myGraph = document.getElementById("myGraph")

let trace1 = {}
trace1.name = "師大"
trace1.mode = "lines+markers"
trace1.type = "scatter"
trace1.marker = {
    size:10
}
trace1.x = []
trace1.y = []

trace1.textposition = "bottom center";
trace1.textfont = {
    family:"Raleway, sans-serif",
    size:10
}

for (let i=0;i<set1.length;i++){
    trace1.x[i] = set1[i][0];
    trace1.y[i] = set1[i][1];
    
}


let trace2 = {}
trace2.name = "台大"
trace2.mode = "lines+markers"
trace2.type = "scatter"
trace2.x = []
trace2.y = []

for (let i=0;i<set2.length;i++){
    trace2.x[i] = set2[i][0];
    trace2.y[i] = set2[i][1];
}


let trace3 = {}
trace3.name = "台科"
trace3.mode = "lines+markers"
trace3.type = "scatter"
trace3.x = []
trace3.y = []

for (let i=0;i<set3.length;i++){
    trace3.x[i] = set3[i][0];
    trace3.y[i] = set3[i][1];
}
let layout = {
    margin:{
        t:40
    },

    title:'三校歷年QS排行',
    yaxis: {
        autorange: 'reversed'
    },
};


let data = [];
data.push(trace1);
Plotly.newPlot(
    myGraph,[trace1,trace2,trace3],layout
);

//2
let myGraph2 = document.getElementById("myGraph2")
let tracea ={}
tracea.type = "bar"
tracea.name = "師大"
tracea.x = []
tracea.y = []

for(let i = 0;i<animals_taipei.length;i++){
    tracea.x[i] = animals_taipei[i]['name']
    tracea.y[i] = animals_taipei[i]['count']
}

let traceb ={}
traceb.type = "bar"
traceb.name = "台大"
traceb.x = []
traceb.y = []

for(let i = 0;i<animals_taoyuan.length;i++){
    traceb.x[i] = animals_taoyuan[i]['name']
    traceb.y[i] = animals_taoyuan[i]['count']
}
let data2=[]
data2.push(tracea);
data2.push(traceb);

let layout2 = {
    margin:{
        t:30,
    },
    title:'台大人數v.s.師大人數',
    
};
Plotly.newPlot(myGraph2,data2,layout2);
//3
let myGraph3 = document.getElementById("myGraph3")
let traceaa = {}
traceaa.type = 'pie'
traceaa.title ="三校系統總人數";
traceaa.labels = []
traceaa.values = []
traceaa.hole = 0.6
for(let i = 0;i<edu_a.length;i++){
    traceaa.labels[i] = edu_a[i]['name']
    traceaa.values[i] = edu_a[i]['count']
}


let data3=[]
data3.push(traceaa);

let layout3 = {
    margin:{
        t:10,
        l:0
    },
    
};
Plotly.newPlot(myGraph3,data3,layout3);