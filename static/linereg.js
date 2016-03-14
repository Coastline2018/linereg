$(document).ready(function(){	
	//get click position, format, and send to drawDot		
	$('#graph').click(function(e){
		var graphMarginLeft = parseInt($('#graph').css('marginLeft'));
		var graphMarginTop = parseInt($('#graph').css('marginTop'));
		var graphHeight = $('#graph').height();
		var graphWidth = $('#graph').width();
		var x = e.pageX-graphMarginLeft;
		var y = e.pageY-graphMarginTop;
		drawDot(e.pageX-4,e.pageY-4,graphHeight);
	});
});

var points = [];
function drawDot(x,y,graphHeight){
	//draw dot for new click on graph
	var newdiv = document.createElement('div');
	newdiv.className = 'newdiv';
	x=x-parseInt($('#graph').css('marginLeft'));
	y=y-parseInt($('#graph').css('marginTop'))
	newdiv.style.marginLeft = x + 'px';
	newdiv.style.marginTop = y + 'px';
	$('#graph').append(newdiv);
	points.push([x+4,graphHeight-y-4]);
}

$(document).on('click','#send_data',function(){
	//send data for processing
	$('#msgbox').html('');
	$('#working').css({'display':'inline-block'});
	var prec = $('#prec_in').val();
	if (! isNaN(prec)){
		$.ajax({
			method:	'post',
			url:	'linereg.py',
			data:	{'package':JSON.stringify([points,prec])},
			success:function(result){
				//receive results
				$('#working').css({'display':'none'});
				if (result.substring(0,2) == 'in'){
					$('#msgbox').html(result);
				}
				else{						
					result = JSON.parse(result);
					var b = parseInt(1000*result[0])/1000.;
					var m = parseInt(1000*result[1])/1000;			
					$('#msgbox').html(	
						'Trendline: y = '+String(m)+'x + '+String(b)+'<br>'+
						'Processing Time: '+result[2]+' s <br>'+
						'Learning rate (alpha): '+result[3]+'<br>'+
						'Iterations to alpha: '+result[4]+'<br>'+
						'Iterations to cost minimization: '+result[5]+'<br>'
					);			
					gen_trend(m,b);
				}
			}
		});
	}
	else{
		$('#working').css({'display':'none'});
		$('#msgbox').html('precision value not a number');
	}
});

function draw_trend(x,y){
	//draw trendline
	var graphHeight = $('#graph').height();
	var dot = document.createElement('div');
	dot.className = 'trendline';
	dot.style.marginLeft = x-2+'px';
	dot.style.marginTop = graphHeight - y -2+ 'px';
	$('#graph').append(dot);	
}

function gen_trend(m,b){
	for (x=0; x<400; x++){
		var y = m*x+b;
		if(0 <= y && y <= 400){
			draw_trend(x,y);
		}	
	}
}

$(document).on('click','#clear',function(){
	$('.newdiv').remove();
	$('.trendline').remove();
	$('#msgbox').html('');
	points=[];
});