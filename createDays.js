/*global $, document*/


var selected = "";
var months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];

var data;

//https://stackoverflow.com/questions/31803300/coloring-the-text-depending-on-numeric-value-using-css
var colorMatch = 
    {
        '0': 'none',
        '1-45': 'bit',
        '46-90': 'medium',
        '91-240': 'alot',
        '241-1440': 'insane'
    };


$(document).ready(function(){
 
    //Load data from JSON
    $.getJSON('data.json',function(dat){
        //console.log(data);
        //console.log(dat["01/01/2020"]);
        data = dat;
        loadData();
        
        
        //Hover stuff
        $("li").hover(function()
        {
            Select($(this));       
        },
        function()
        {
            Deselect($(this));
        });


        //Click stuff
        $("li").click(function(){
            OnClick($(this));
        });

        
        //Adds colour to days where netflix was watched
        $('li').each(function(index)
        {
            var currentKey = "0";
            for(var key in colorMatch)
            {
                if(colorMatch.hasOwnProperty(key))
                {
                    var min = key.split("-")[0];
                    var max = key.split("-")[1];
                    
                    var value = parseInt($(this).get(0).getAttribute("wt"));
                    
                    if( min <= value && value <= max)
                    {
                        currentKey = key;
                    }
                }
            }
            if(currentKey != "0")
            {
                $(this).addClass(colorMatch[currentKey]);
            }
            
        });
        
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
        
        
        var mont = month[1];
        var day = i;
        //Formatting for json
        if (day < 10)
        {
            day = "0"+day;
        }
        if (mont < 10)
        {
            mont = "0"+mont;
        }
        
      
        var date = day+"/"+mont+"/"+year;
        
        
        
        //Gets watchtime data
        var watchTime;
        
        if (data.hasOwnProperty(date))
        {
            watchTime = data[date]["duration"];
            //console.log(data[date]["duration"]);
        }
        else
        {
            watchTime = 0;
        }
        
        
        
        str += '<li wt= "'+watchTime+'">'+i+'</li>\n';
    }
    str += '</ul>';
    
   return str
}


function OnClick(obj)
{

    var month = obj.parent().get(0).getAttribute("value");
    var day = obj.val();
    var year = obj.parent().parent().get(0).getAttribute("id");
    //Formatting for json
    if (day < 10)
    {
        day = "0"+day;
    }
    if (month < 10)
    {
        month = "0"+month;
    }
    
    var date = day+"/"+month+"/"+year;
    selected = date;

    
    
    
    //Display data on day that was clicked on
    if(data.hasOwnProperty(selected))
    {
        console.log(data[selected]);
        $("#day").text(data[selected]["duration"]);
    }
    else
    {
        $("#day").text("You didn't watch anything on the "+selected);
    }
    
    
}



function loadData()
{
    
    //Fetch years
    var years = [];
            
    for (var key in data) 
    {
        if (data.hasOwnProperty(key)) 
        {
            //console.log(key + " -> " + data[key]);
            
            var year = key.split("/")[2];
            if (years.includes(year) == false)
            {
                years.push(year);
            }
        }
    }
    //Sorts years
    years = years.sort();

    
    /*Calculate First year start offset and Last year end offset
    
    e.g Mar 17 -> Jan 20
    
    */
    var smallestMonth = 12;
    var largestMonth = 1;
    for (var key in data) 
    {
        if (data.hasOwnProperty(key)) 
        {
            //console.log(key + " -> " + data[key]);
            
            var year = key.split("/")[2];
            var month = key.split("/")[1];
            if (year == years[0] && month < smallestMonth)
            {
                smallestMonth = month;
            }
            if (year == years[year.length-1] && month > largestMonth)
            {
                largestMonth = month;
            }
        }
    }
    
    //Create months
    for(var j=0; j < years.length; j++)
    {
        
        $("#years").append('<div id='+years[j]+'></div>');
        
        //For month offsets
        var start = 0;
        var end = 12;
        
        if(j == 0)
        {
            start = smallestMonth-1;
        }
        if(j == year.length-1)
        {
            end = largestMonth;
        }
        
        
        for(var i= start; i <end; i++)
        {
            $("#"+years[j]).append(createMonth([months[i],i+1],30,years[j]));
        }
    }
}

