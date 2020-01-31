/*global $, document*/


var selected = "";

$(document).ready(function(){

    
    //Create months
    var months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];
    var years = [2017,2018,2019,2020];
    
    for(var j=0; j < 1; j++)
    {
        
        $("#years").append('<div id='+years[j]+'></div>');
        
        for(var i= 0; i <6; i++)
        {
            $("#"+years[j]).append(createMonth([months[i],i+1],30,years[j]));
        }
    }

    
    
    //Hover stuff
    $("li").hover(function(){
        Select($(this));       
    },function(){
        Deselect($(this));
    });
    
    
    //Click stuff
    $("li").click(function(){
        OnClick($(this));
    });
    
});

function Select(obj)
{
    obj.val(obj.text());
    obj.html('<span class="active">'+obj.text()+'</span>');
}

function Deselect(obj)
{
     obj.html(obj.val());
}

function createMonth(month,days,year)
{
    //Year as string and last to chars e.g 2019 -> 19
    var yearStr = String(year).charAt(String(year).length-2)+String(year).charAt(String(year).length-1);
    
    var str = '<ul value="'+month[1]+'" class="days"> \n <p class="month">'+month[0]+' '+yearStr+'</p>';
    
    for (var i = 1; i <= days; i++) {
      str += '<li>'+i+'</li>\n';
    }
    str += '</ul>'
    //console.log(str);
   return str
}


function OnClick(obj)
{
    //alert(obj.parent().parent().val()+" the "+obj.val());
    
    var month = obj.parent().get(0).getAttribute("value");
    var day = obj.val();
    var year = obj.parent().parent().get(0).getAttribute("id");
    //Formatting for json
    if (day < 10)
    {
        day = "0"+day;
    }
    
    var date = day+"/"+month+"/"+year;
    selected = date;
    //alert(date);
    
    $("#day").text(selected);
}
