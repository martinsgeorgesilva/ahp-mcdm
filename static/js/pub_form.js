setTimeout(function () {
    let len = document.getElementById('len_relations').value;
    console.log(len, 'lala')
    $("#btn-green").hide()
    $("#btn-red").hide()
    $("#btn").hide()
    $("#help-div").hide();


    for (x = 0; x < len; x++) {
        let input = document.getElementById('range_' + x.toString());
        let span = document.getElementById('span_' + x.toString());
        document.getElementById('range_' + x.toString()).addEventListener('change', (event) => {
            let name1 = input.dataset.name1
            let name2 = input.dataset.name2
            input.value = event.target.value;
            span.innerHTML = returnOutput(event.target.value, name1, name2);
            submitForm();
        });
        span.innerHTML = 'Considero que <b>' + input.dataset.name1 + '</b> seja tão importante quanto <b>' + input.dataset.name2 + '</b>'
    }
    submitForm();
}, 1000);


function submitForm() {
    var formElements = document.getElementById("my_form").elements;
    var postData = {};
    for (var i = 0; i < formElements.length; i++)
        if (formElements[i].type != "submit")//we dont want to include the submit-buttom
            postData[formElements[i].name] = formElements[i].value;
    $.ajax({
        url: '/ajax-post',
        type: 'POST',
        data: JSON.stringify(postData),
        contentType: false,
        cache: false,
        processData: false
    }).done(function (response) {
        let resp = JSON.parse(response)
        console.log(resp)
        $("#abc").attr('class', '');
        let showData;
        if (resp.inconsistencia > 10) {

            $("#btn-green").hide();
            $("#btn-red").show();
            $("#btn").hide();
            $('#help-text').html('respostas malajeitadas <strong>black sheep</strong>');
            showData = false;
        }
        else {
            showData = true;
            $("#btn-green").show()
            $("#btn-red").hide()
            $('#help-text').html('respostas boas <strong>white          sheep</strong>');
            $("#btn").show();
        }
        let cat = new Array();
        let values = new Array();
        Object.entries(resp.prioridades).forEach(([key, value]) => {
            cat.push(key);
            values.push(value * 100);
        });
        $("#help-div").hide();

        chart.update({
            xAxis: {
                categories: cat
            },
            series: [{
                data: values
            }]
        })
        chart.redraw();

        $("#ci1").html(resp.inconsistencia);
        $("#ci2").html(resp.inconsistencia);
    });
}

function fakeSubmit() {
    Swal.fire('Apenas testando o formulário')
}

function returnOutput(value, name1, name2) {
    console.log(value)
    switch (value) {
        case '0':
            return 'Considero que <b>' + name1 + '</b> seja <span style="color:red">extremamente</span> mais importante que <b>' + name2 + '</b>'
            break;
        case '1':
            return 'Considero que <b>' + name1 + '</b> seja <span style="color:red">extremamente</span> mais importante que <b>' + name2 + '</b>'
            break;
        case '2':
            return 'Considero que <b>' + name1 + '</b> seja <span style="color:red">claramente</span> mais importante que <b>' + name2 + '</b>'
            break;
        case '3':
            return 'Considero que <b>' + name1 + '</b> seja <span style="color:red">claramente</span> mais importante que <b>' + name2 + '</b>'
            break;
        case '4':
            return 'Considero que <b>' + name1 + '</b> seja <span style="color:red">moderadamente</span> mais importante que <b>' + name2 + '</b>'
            break;
        case '5':
            return 'Considero que <b>' + name1 + '</b> seja <span style="color:red">moderadamente</span> mais importante que <b>' + name2 + '</b>'
            break;
        case '6':
            return 'Considero que <b>' + name1 + '</b> seja <span style="color:red">ligeiramente</span> mais importante que <b>' + name2 + '</b>'
            break;
        case '7':
            return 'Considero que <b>' + name1 + '</b> seja <span style="color:red">ligeiramente</span> mais importante que <b>' + name2 + '</b>'
            break;
        case '8':
            return 'Considero que <b>' + name1 + '</b> seja  tão importante quanto <b>' + name2 + '</b>'
            break;
        case '9':
            return 'Considero que <b>' + name2 + '</b> seja <span style="color:red">ligeiramente</span> mais importante que <b>' + name1 + '</b>'

            break;
        case '10':
            return 'Considero que <b>' + name2 + '</b> seja <span style="color:red">ligeiramente</span> mais importante que <b>' + name1 + '</b>'
            break;
        case '11':
            return 'Considero que <b>' + name2 + '</b> seja <span style="color:red">moderadamente</span> mais importante que <b>' + name1 + '</b>'
            break;
        case '12':
            return 'Considero que <b>' + name2 + '</b> seja <span style="color:red">moderadamente</span> mais importante que <b>' + name1 + '</b>'
            break;
        case '13':
            return 'Considero que <b>' + name2 + '</b> seja <span style="color:red">claramente</span> mais importante que <b>' + name1 + '</b>'
            break;
        case '14':
            return 'Considero que <b>' + name2 + '</b> seja <span style="color:red">claramente</span> mais importante que <b>' + name1 + '</b>'
            break;
        case '15':
            return 'Considero que <b>' + name2 + '</b> seja <span style="color:red">extremamente</span> mais importante que <b>' + name1 + '</b>'
            break;
        case '16':
            return 'Considero que <b>' + name2 + '</b> seja <span style="color:red">extremamente</span> mais importante que <b>' + name1 + '</b>'
            break;
    }
}

var chart;

setTimeout(function () {
    chart = Highcharts.chart('container', {
        chart: {
            type: 'column',
            backgroundColor: "#fff"

        },
        credits: {
            enabled: false
        },
        title: {
            text: ''
        },
        subtitle: {
            text: ''
        },
        xAxis: {
            categories: []
        },
        series: [{
            type: 'column',
            colorByPoint: true,
            data: [],
            showInLegend: false
        }],
        yAxis: {
            labels: {
                enabled: false
            },
            title: {
                text: null
            }
        },
        legend: {
            enabled: false
        },
        plotOptions: {
            series: {
                borderWidth: 0,
                dataLabels: {
                    enabled: true,
                    format: '{point.y:.1f}%'
                }
            }
        },

        tooltip: {
            enabled: false
            // headerFormat: '<span style="font-size:11px">{point.category}</span><br>',
            // pointFormat: '<b>{point.y:.2f}%</b> de preferência<br/>'
        },
    });
}, 1000);
