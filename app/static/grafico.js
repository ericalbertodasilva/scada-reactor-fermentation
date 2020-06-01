google.charts.load('current', {'packages':['corechart']});
google.charts.setOnLoadCallback(drawChart);

var data_graf1, data_graf2, data_graf3, data_graf4;
var options1, options2, options3, options4;
var chart_data1, chart_data2, chart_data3, chart_data4;
var grafico_inicial1, grafico_inicial2, grafico_inicial3, grafico_inicial4;
var temperatura = [0,0];
var UR = [0,0];
var reator1 = [0,0,0,0];
var reator2 = [0,0,0,0];
var t1=1;

function drawChart() {
    data_graf1 = new google.visualization.DataTable();
    data_graf1.addColumn('date', 'tempo');
    data_graf1.addColumn('number', 'Temperatura');
    data_graf2 = new google.visualization.DataTable();
    data_graf2.addColumn('date', 'tempo');
    data_graf2.addColumn('number', 'UR');
    data_graf3 = new google.visualization.DataTable();
    data_graf3.addColumn('date', 'tempo');
    data_graf3.addColumn('number', 'CO2');
    data_graf3.addColumn('number', 'ART');
    data_graf3.addColumn('number', 'Etanol');
    data_graf4 = new google.visualization.DataTable();
    data_graf4.addColumn('date', 'tempo');
    data_graf4.addColumn('number', 'CO2');
    data_graf4.addColumn('number', 'ART');
    data_graf4.addColumn('number', 'Etanol');
    options1 = {
        pointSize: 2,
        hAxis: {
            title: 'Tempo',
            gridlines: {
              count: -1
            }
        },
        vAxis: {
            title: '°C',
        },
        title: "Gráfico da Temperatura",
        crosshair: {
            color: '#000',
            trigger: 'selection'
        },
        legend: {position:"top"}
    };
    options2 = {
        pointSize: 2,
        hAxis: {
            title: 'Tempo',
            gridlines: {
              count: -1
            }
        },
        vAxis: {
            title: '%',
        },
        title: "Gráfico da Umidade",
        crosshair: {
            color: '#000',
            trigger: 'selection'
        },
        legend: {position:"top"}
    };
    options3 = {
        pointSize: 2,
        hAxis: {
            title: 'Tempo',
            gridlines: {
              count: -1
            }
        },
        vAxis: {
            title: 'CO2',
        },
        title: "Gráfico de Reator 1",
        crosshair: {
            color: '#000',
            trigger: 'selection'
        },
        legend: {position:"top"}
    };
    options4 = {
        pointSize: 2,
        hAxis: {
            title: 'Tempo',
            gridlines: {
              count: -1
            }
        },
        vAxis: {
            title: 'CO2',
        },
        title: "Gráfico de Reator 2",
        crosshair: {
            color: '#000',
            trigger: 'selection'
        },
        legend: {position:"top"}
    };
    var chart1 = new google.visualization.LineChart(document.getElementById('curve_chart1'));
    chart1.draw(data_graf1, options1);
    var chart2 = new google.visualization.LineChart(document.getElementById('curve_chart2'));
    chart2.draw(data_graf2, options2);
    var chart3 = new google.visualization.LineChart(document.getElementById('curve_chart3'));
    chart3.draw(data_graf3, options3);
    var chart4 = new google.visualization.LineChart(document.getElementById('curve_chart4'));
    chart4.draw(data_graf4, options4);
};
    $(document).ready(function() {
        setInterval(function () {
            if (t1==1){
                $.get('http://127.0.0.1:5000/_get_grafico',function(data2) {
                    grafico_inicial1=JSON.parse(data2);
                    /*
                    t1 = new Date(graf[graf.length-1]["data_registro"]);
                    t0 = new Date(graf[graf.length-31]["data_registro"]);
                    deltat=t1.getTime() - t0.getTime();
                    der1 = (parseFloat(graf[graf.length-1]['reator_CO2_1']) - parseFloat(graf[graf.length-31]['reator_CO2_1']))*1000/deltat;
                    der2 = (parseFloat(graf[graf.length-1]['reator_CO2_2']) - parseFloat(graf[graf.length-31]['reator_CO2_2']))*1000/deltat;
                    $("#der1").val(parseFloat(der1));
                    $("#der2").val(parseFloat(der2));
                    */
                    for(var i = 0; i < grafico_inicial1.length; i++) {
                        temperatura[0]=new Date(grafico_inicial1[i]["data_registro"]);
                        temperatura[1]=parseFloat(grafico_inicial1[i]["temperatura"]);
                        UR[0]=new Date(grafico_inicial1[i]["data_registro"]);
                        UR[1]=parseFloat(grafico_inicial1[i]["UR"]);
                        data_graf1.addRow(temperatura);
                        data_graf2.addRow(UR);
                    };
                    var chart1 = new google.visualization.LineChart(document.getElementById('curve_chart1'));
                    chart1.draw(data_graf1, options1);
                    var chart2 = new google.visualization.LineChart(document.getElementById('curve_chart2'));
                    chart2.draw(data_graf2, options2);
                });
                $.get('http://127.0.0.1:5000/_get_grafico_reator1',function(data2) {
                    grafico_inicial3=JSON.parse(data2);
                    for(var i = 0; i < grafico_inicial3.length; i++) {
                        reator1[0]=new Date(grafico_inicial3[i]["data_registro"]);
                        reator1[1]=parseFloat(grafico_inicial3[i]["co2"]);
                        reator1[2]=parseFloat(grafico_inicial3[i]["art_estimado"]);
                        reator1[3]=parseFloat(grafico_inicial3[i]["etanol_estimado"]);
                        data_graf3.addRow(reator1);
                    };
                    var chart3 = new google.visualization.LineChart(document.getElementById('curve_chart3'));
                    chart3.draw(data_graf3, options3);
                });
                $.get('http://127.0.0.1:5000/_get_grafico_reator2',function(data) {
                    grafico_inicial4=JSON.parse(data);
                    for(var i = 0; i < grafico_inicial4.length; i++) {
                        reator2[0]=new Date(grafico_inicial4[i]["data_registro"]);
                        reator2[1]=parseFloat(grafico_inicial4[i]["co2"]);
                        reator2[2]=parseFloat(grafico_inicial4[i]["art_estimado"]);
                        reator2[3]=parseFloat(grafico_inicial4[i]["etanol_estimado"]);
                        data_graf4.addRow(reator2);
                    };
                    var chart4 = new google.visualization.LineChart(document.getElementById('curve_chart4'));
                    chart4.draw(data_graf4, options4);
                });
                t1=0;
            };

            $.get('http://127.0.0.1:5000/_get_status', function(data1) {
                grafico_inicial1=data1;
                $("#temperatura").val(parseFloat(grafico_inicial1['temperatura']));
                $("#UR").val(parseFloat(grafico_inicial1['UR']));
                if (new Date(grafico_inicial1["data_registro"])  != temperatura[0]) {
                    temperatura[0]=new Date(grafico_inicial1["data_registro"]);
                    temperatura[1]=parseFloat(grafico_inicial1['temperatura']);
                    UR[0]=new Date(grafico_inicial1["data_registro"]);
                    UR[1]=parseFloat(grafico_inicial1['UR']);
                    data_graf1.addRow(temperatura);
                    data_graf2.addRow(UR);
                    var chart1 = new google.visualization.LineChart(document.getElementById('curve_chart1'));
                    chart1.draw(data_graf1, options1);
                    var chart2 = new google.visualization.LineChart(document.getElementById('curve_chart2'));
                    chart2.draw(data_graf2, options2);
                }
            });
            $.get('http://127.0.0.1:5000/_get_status_reator1', function(data1) {
                grafico_inicial3=data1;
                $("#reator1_co2").val(reator1[1]);
                //$("#reator1_art_estimado").val(reator1[2]);
                //$("#retaor1_etanol_estimado").val(reator1[3]);

                
                if (new Date(grafico_inicial3["data_registro"])  != reator1[0]) {
                    reator1[0]=new Date(grafico_inicial3["data_registro"]);
                    reator1[1]=parseFloat(grafico_inicial3["co2"]);
                    reator1[2]=parseFloat(grafico_inicial3["art_estimado"]);
                    reator1[3]=parseFloat(grafico_inicial3["etanol_estimado"]);
                    var chart3 = new google.visualization.LineChart(document.getElementById('curve_chart3'));
                    chart3.draw(data_graf3, options3);
                }
            });
        }, 5000);

        setInterval(function () {
            $.get('http://127.0.0.1:5000/_get_status_reator2', function(data1) {
                grafico_inicial4=data1;
                $("#reator2_co2").val(reator2[1]);
                //$("#reator2_art_estimado").val(reator2[1]);
                //$("#retaor2_etanol_estimado").val(reator2[1]);

                
                if (new Date(grafico_inicial4["data_registro"])  != reator2[0]) {
                    reator2[0]=new Date(grafico_inicial4["data_registro"]);
                    reator2[1]=parseFloat(grafico_inicial4["co2"]);
                    reator2[2]=parseFloat(grafico_inicial4["art_estimado"]);
                    reator2[3]=parseFloat(grafico_inicial4["etanol_estimado"]);
                    var chart4 = new google.visualization.LineChart(document.getElementById('curve_chart4'));
                    chart4.draw(data_graf4, options4);
                }
            });
        }, 5000);
    });
    setTimeout(function(){ location.reload(); }, 600000);

    // 2019-12-09 10:00:00.000000