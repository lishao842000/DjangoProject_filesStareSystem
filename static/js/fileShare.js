/**
 * Created by Administrator on 2015-09-14.
 */
$(function(){
			    var old_X = 0, new_X = 0, move_X = 0, is_mouse_down = false, Width = 200;
			    $(".expander")
			    .mousedown(function(e){
			        old_X = e.pageX;
			        is_mouse_down = true;
			    });
			    $(document).bind("click mouseup",function(e){
			        if(is_mouse_down){
			          is_mouse_down = false;
			        }
			    })
			    .mousemove(function(e){
			        new_X = e.pageX;
			        move_X = new_X - old_X;
			        old_X = new_X;
			        Width = $(".left").width() + move_X;
			        if(is_mouse_down){
			            $(".left").css("width", Width > 200 ? Width : 200);
			        }
			    });
			});
