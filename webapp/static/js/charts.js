/* CCMS Chart rendering using Apache ECharts */

/**
 * Render a bar chart in the given DOM element.
 * @param {string} elementId - The DOM element ID
 * @param {Array} data - Array of {name, value} objects
 * @param {string} title - Chart title
 */
function renderBarChart(elementId, data, title) {
    const chart = echarts.init(document.getElementById(elementId));
    const option = {
        title: {
            text: title,
            left: "center",
            textStyle: { fontSize: 14 }
        },
        tooltip: { trigger: "axis" },
        xAxis: {
            type: "category",
            data: data.map(d => d.name),
        },
        yAxis: {
            type: "value",
            minInterval: 1,
        },
        series: [{
            type: "bar",
            data: data.map(d => d.value),
            itemStyle: {
                color: function(params) {
                    const colors = ["#5470c6", "#91cc75", "#fac858", "#ee6666"];
                    return colors[params.dataIndex % colors.length];
                }
            },
            label: {
                show: true,
                position: "top"
            }
        }]
    };
    chart.setOption(option);
    window.addEventListener("resize", () => chart.resize());
}

/**
 * Render a pie chart in the given DOM element.
 * @param {string} elementId - The DOM element ID
 * @param {Array} data - Array of {name, value} objects
 * @param {string} title - Chart title
 */
function renderPieChart(elementId, data, title) {
    const chart = echarts.init(document.getElementById(elementId));
    const option = {
        title: {
            text: title,
            left: "center",
            textStyle: { fontSize: 14 }
        },
        tooltip: {
            trigger: "item",
            formatter: "{b}: {c} ({d}%)"
        },
        legend: {
            orient: "vertical",
            left: "left"
        },
        series: [{
            type: "pie",
            radius: "60%",
            data: data.filter(d => d.value > 0),
            emphasis: {
                itemStyle: {
                    shadowBlur: 10,
                    shadowOffsetX: 0,
                    shadowColor: "rgba(0, 0, 0, 0.5)"
                }
            },
            label: {
                formatter: "{b}: {c}"
            }
        }]
    };
    chart.setOption(option);
    window.addEventListener("resize", () => chart.resize());
}
