$(document).ready(function(){
    $.get("api")
    .done(function(data){
        $(".info-tickets-total").html(parseInt(data.total_shows))
        $(".info-shows-total").html(parseInt(data.total_tickets))
        $(".info-earnings-total").html("$" + parseFloat(data.total_earnings))
        
        $(".info-tickets-arrow").removeClass("up").removeClass("down").addClass(data.tickets_growth ? "up" : "down")
        $(".info-shows-arrow").removeClass("up").removeClass("down").addClass(data.shows_growth ? "up" : "down")
        $(".info-earnings-arrow").removeClass("up").removeClass("down").addClass(data.earnings_growth ? "up" : "down")

        $(".info-tickets-percentage").html(parseFloat(data.tickets_percentage) + "%")
        $(".info-shows-percentage").html(parseFloat(data.shows_percentage) + "%")
        $(".info-earnings-percentage").html(parseFloat(data.earnings_percentage) + "%")

        loadLibGraphStats(data)
    })
})

function loadLibGraphStats(data) {
    google.charts.load('current', {'packages': ['corechart']});
    google.charts.setOnLoadCallback(drawAgeDistributionChart);
    google.charts.setOnLoadCallback(drawMovieDistributionChart);

    function drawAgeDistributionChart() {
        var raw_data = [
            [data.age_distribution.title, data.age_distribution.param],
        ]
        for(var key in data.age_distribution.values){
            raw_data.push([key, data.age_distribution.values[key]])
        }
        var chart_data = google.visualization.arrayToDataTable(raw_data);

        // Optional; add a title and set the width and height of the chart
        var options = {
            'title': data.age_distribution.title,
            titleTextStyle: {fontSize: 15, fontName: 'Source Sans Pro', regular: true},
            pieHole: 0.58, 'width': 400, 'height': 250,
            colors: ['#55D9FD', '#FE8575', '#FFD983', '#A49DFF', '#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5', '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f', '#c7c7c7', '#bcbd22', '#dbdb8d', '#17becf', '#9edae5'],
            backgroundColor: '#FEFCFF',
            legend: {
                position: 'right',
                alignment: 'center',
                textStyle: {fontSize: 11, fontName: 'Source Sans Pro', regular: true}
            }, pieSliceText: 'none'
        };
        // Display the chart inside the <div> element with id="piechart"
        var chart = new google.visualization.PieChart(document.getElementById('Age_chart_div'));
        chart.draw(chart_data, options);
    }

    // Draw the chart and set the chart values
    function drawMovieDistributionChart() {
        var raw_data = [
            [data.movie_distribution.title, data.movie_distribution.param],
        ]
        for(var key in data.movie_distribution.values){
            raw_data.push([key, data.movie_distribution.values[key]])
        }
        var chart_data = google.visualization.arrayToDataTable(raw_data);

        // Optional; add a title and set the width and height of the chart
        var options = {
            'title': data.movie_distribution.title,
            titleTextStyle: {fontSize: 15, fontName: 'Source Sans Pro', regular: true},
            pieHole: 0.58,
            'width': 400,
            'height': 250,
            colors: ['#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5', '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f', '#c7c7c7', '#bcbd22', '#dbdb8d', '#17becf', '#9edae5'],
            backgroundColor: '#FEFCFF',
            legend: {
                position: 'right',
                alignment: 'center',
                textStyle: {fontSize: 11, fontName: 'Source Sans Pro', regular: true}
            },
            pieSliceText: 'none'
        };

        // Display the chart inside the <div> element with id="piechart"
        var chart = new google.visualization.PieChart(document.getElementById('Movie_chart_div'));
        chart.draw(chart_data, options);
    }
}
