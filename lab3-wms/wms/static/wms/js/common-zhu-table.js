function zhu_table_gen(subtitle_text, head_text, table_name, name_list, dataList, container_id, element_list) {
   var chart = {
      type: 'column'
   };
   var title = {
      text: head_text   
   };
   var subtitle = {
      text: subtitle_text  
   };
   var xAxis = {
      categories: name_list,
      crosshair: true
   };
   var yAxis = {
      min: 0,
      title: {
         text: table_name         
      }      
   };
   var tooltip = {
      headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
      pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
         '<td style="padding:0"><b>{point.y:.1f} mm</b></td></tr>',
      footerFormat: '</table>',
      shared: true,
      useHTML: true
   };
   var plotOptions = {
      column: {
         pointPadding: 0.2,
         borderWidth: 0
      }
   };  
   var credits = {
      enabled: false
   };
   
   var series = [];
   var element_length = element_list.length;
   for (var i = 0; i < element_length; ++i) {
       series.push({name: element_list[i], data: dataList[i]});
   }
      
   var json = {};   
   json.chart = chart; 
   json.title = title;   
   json.subtitle = subtitle; 
   json.tooltip = tooltip;
   json.xAxis = xAxis;
   json.yAxis = yAxis;  
   json.series = series;
   json.plotOptions = plotOptions;  
   json.credits = credits;
   $(container_id).highcharts(json);
}
   