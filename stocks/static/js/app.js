function create_graph(key, value, chart_type, label, id, x_quote=false, x_apostrophe=false, y_quote=false, y_apostrophe=false) {
    temp = key;
    if (x_quote) {
        x_Values = JSON.parse(temp.replace(/&quot;/g,'"'));
    } else if (x_apostrophe) {
        x_Values = JSON.parse(temp.replace(/&#x27;/g,'"'));
    } else {
        x_Values = JSON.parse(temp);;
    }

    temp = value;
    console.log(temp);
    if (y_quote) {
        y_Values = JSON.parse(temp.replace(/&quot;/g,'"'));
    } else if (y_apostrophe) {
        y_Values = JSON.parse(temp.replace(/&#x27;/g,'"'));
    } else {
        y_Values = JSON.parse(temp);
    }
        
    var backgroundColor = [];
    var borderColor = [];
    const current_year = new Date().getFullYear();
    for(i = 0; i < x_Values.length; i++) {
        if (parseInt(x_Values[i]) > current_year) {
            backgroundColor.push("rgba(144, 163, 191, 1)");
            borderColor.push("rgba(144, 163, 191, 1)");
        } else {
            backgroundColor.push("rgba(124, 92, 252, 1.0)");
            borderColor.push("rgba(124, 92, 252, 1.0)");
        }
    }
    
    const ctx = document.getElementById(id).getContext('2d');
    const chart = new Chart(ctx, {
    type: chart_type,
    data: {
        labels: x_Values,
        datasets: [{
            label: label,
            data: y_Values,
            backgroundColor: backgroundColor,
            borderColor: borderColor,
            fill: false,
        }]
    },
    options: {
        spanGaps: true,
        animation: false,
        pointRadius: 0,
    }
    });
}