var map;

function map_init(center, zoom){
    return new AMap.Map('map', {
        resizeEnable: true,
        zoom:zoom,
        center: center,
        lang:'en'
    });
}


function scatter(map, data){
           var styleArr = [{
             url: '/static/leaflet/images/marker-icon.png',
             size: new AMap.Size(11, 11),
             anchor: new AMap.Pixel(5,5)
           },
           {
             url: '/static/leaflet/images/map-marker-icon.png',
             size: new AMap.Size(11, 11),
             anchor: new AMap.Pixel(5,5)
           }
           ];
           var massMarks = new AMap.MassMarks(data, {
                zIndex: 5,
                zooms: [3, 19],
                style: styleArr
           });
           var marker = new AMap.Marker({content: ' ', map: map});
           massMarks.on('mouseover', function (e) {
           marker.setPosition(e.data.lnglat);
           marker.setLabel({content: 'room: ' + e.data.name + '<br />price:' + e.data.price + '<br />id:' + e.data.id})
           });
           massMarks.setMap(map);
}

function drawgraph(id, datax, datay, tex)
{
    var barchart = echarts.init(document.getElementById(id));
    var option = {
                     title:{
                       text:tex
                    },
                    xAxis: {
                    type: 'category',
                    data: datax
                    },
                    yAxis: {
                    type: 'value'
                    },
                    series: [{
                    data: datay,
                    type: 'line'
                    }],
                    grid:{
                         x:50,
                    }
                    };
    barchart.setOption(option);
}

function initMap(ct)
{
    map = new google.maps.Map(
      document.getElementById('map'), {zoom: 12, center: ct});
    return map;
}

function attach(mk, content)
{
    var infowindow = new google.maps.InfoWindow({
          content: content
    })
    google.maps.event.addListener(mk, 'click', function(){
         infowindow.open(map, mk);
       });
}

function scatterMap(map, data)
{
   var styleArr = [{
             url: '/static/leaflet/images/011.png',
             size: new google.maps.Size(6, 6),
             anchor: new google.maps.Point(8, 8),
             origin: new google.maps.Point(0, 0),
           },
           {
             url: '/static/leaflet/images/013.png',
             size: new google.maps.Size(6, 6),
             anchor: new google.maps.Point(8, 8),
             origin: new google.maps.Point(0, 0),
           },
           {
             url: '/static/leaflet/images/014.png',
             size: new google.maps.Size(6, 6),
             anchor: new google.maps.Point(8, 8),
             origin: new google.maps.Point(0, 0),
           },
           {
             url: '/static/leaflet/images/map-marker-icon.png',
             size: new google.maps.Size(16, 16),
             anchor: new google.maps.Point(256, 512),
           },
           {
             url: '/static/leaflet/images/bullet_purple.png',
             size: new google.maps.Size(12, 12),
             anchor: new google.maps.Point(6, 6),
             origin: new google.maps.Point(0, 0),
           },
           ];
   var plus = 0;
   for(var i=0;i<data.length;i++)
   {
       var latlng={lat:data[i].lnglat[0], lng:data[i].lnglat[1]};
       var type=data[i].style;
       if(data[i].style==3)
           type=5;
       var contentString = 'Room: ' + data[i].name + '<br />Price:' + data[i].price + '<br />ID:' + data[i].id
                           + '<br />Link: ' + '<a href:\"https://www.airbnb.com/room/' + data[i].id +
                           '\" >'+data[i].name + '</a>';
       var marker=new google.maps.Marker({
          position: latlng,
          map: map,
          title: data[i].name,
          icon: styleArr[type],
        });
       if(type==1)
           plus++;
       /*var infowindow = new google.maps.InfoWindow({
          content: contentString
        });*/
       attach(marker, contentString);
       markers.push(marker);
   }
   /*var percent = int(1.0*plus/data.length*100);//to do list
   var bar = document.getElementsByName("plus")[0];
   bar.style.width=percent.toString()+"%";
   var nobar = document.getElementsByName("nonplus")[0];
   nobar.style.width=(100-percent).toString() + "%";*/
}

function initTime(cityname)
{
    var opt=document.getElementsByName("time")[0];
    opt.innerHTML = "";
    if(cityname == 'london')
        var time=ld;
    else if(cityname == 'sydney')
        var time=sy;
    else if(cityname == 'sanfrancisco')
        var time=sf;
    for(var i=0;i<time.length;i++)
    {
        var objOption = document.createElement("OPTION");
        objOption.text = time[i];
        objOption.value = time[i];
        objOption.name = "time-option";
        opt.options.add(objOption);
    }
    opt.options[0].selected = true;
}

function reLoad()
{
    var gp = document.getElementById("graph-container");
    gp.innerHTML="<div>Loading...</div>";
    var tb = document.getElementById("stat");
    tb.innerHTML="Loading...";
    var cp = document.getElementsByName("com-panel")[0];
    cp.innerHTML="Loading...";
}

function reGraph(graph)
{
    var gp = document.getElementById("graph-container");
    gp.innerHTML='<div id="' + graph[0] + '" style="width:85%;height:200px;"></div>';
    drawgraph(graph[0], graph[1], graph[2], graph[0]);
}

function rePanel(data)
{
    var cp = document.getElementsByName("com-panel")[0];
    cp.innerHTML="";
    var ctt = data;
    cp.innerHTML=ctt;
}