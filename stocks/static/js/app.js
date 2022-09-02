var jQueryScript = document.createElement('script');  
jQueryScript.setAttribute('src','https://cdn.jsdelivr.net/npm/chartjs-plugin-datalabels@2.0.0');
document.head.appendChild(jQueryScript);

function create_graph(key, value, chart_type, label, id, x_quote = false, x_apostrophe = false, y_quote = false, y_apostrophe = false) {
    temp = key;
    if (x_quote) {
        x_Values = JSON.parse(temp.replace(/&quot;/g, '"'));
    } else if (x_apostrophe) {
        x_Values = JSON.parse(temp.replace(/&#x27;/g, '"'));
    } else {
        x_Values = JSON.parse(temp);;
    }

    temp = value;
    if (y_quote) {
        y_Values = JSON.parse(temp.replace(/&quot;/g, '"'));
    } else if (y_apostrophe) {
        y_Values = JSON.parse(temp.replace(/&#x27;/g, '"'));
    } else {
        if (temp.length === 0) {
            y_Values = new Array(x_Values.length).fill(0)
        } else {
            y_Values = JSON.parse(temp);
        }
    }

    var backgroundColor = [];
    var borderColor = [];
    const current_year = new Date().getFullYear();
    for (i = 0; i < x_Values.length; i++) {
        if (parseInt(x_Values[i]) > current_year) {
            backgroundColor.push("rgba(144, 163, 191, 1)");
            borderColor.push("rgba(144, 163, 191, 1)");
        } else {
            backgroundColor.push("rgba(124, 92, 252, 1.0)");
            borderColor.push("rgba(124, 92, 252, 1.0)");
        }
    }

    params = null;
    if (chart_type == "bar") {
        params = {
            datalabels: {
                color: '#ffffff',
                anchor: 'center',
                align: 'center',
                formatter: function(value) {               
                    return (Math.round(value*100)/100).toFixed(1);
                },
                font: {
                    weight: 'bold'
                }
            }
        };
    } else {
        params = {
            datalabels: {
                color: '',
            }
        };
    }

    const ctx = document.getElementById(id).getContext('2d');
    const chart = new Chart(ctx, {
        type: chart_type,
        plugins: [ChartDataLabels],
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
            plugins: params
        }
    });
}