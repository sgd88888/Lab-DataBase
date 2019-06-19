function pie_table_gen(head_text, pie_name, dataList, container_id) {
   var chart = {
       plotBackgroundColor: null,
       plotBorderWidth: null,
       plotShadow: false
   };
   var title = {
      text: head_text   
   };      
   var tooltip = {
      pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
   };
   var plotOptions = {
      pie: {
         allowPointSelect: true,
         cursor: 'pointer',
         dataLabels: {
            enabled: true,
            format: '<b>{point.name}%</b>: {point.percentage:.1f} %',
            style: {
               color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
            }
         }
      }
   };

   var series= [{
      type: 'pie',
      name: pie_name,
      data: dataList
   }];    

   var json = {};   
   json.chart = chart; 
   json.title = title;     
   json.tooltip = tooltip;  
   json.series = series;
   json.plotOptions = plotOptions;
   $(container_id).highcharts(json);  
}
