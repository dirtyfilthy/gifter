function get_user(user_id){
	
}


$(document).ready(function (){
	$("#user_search").autocomplete({
		source: "/user_search",
		delay: 500,
		minLength: 3,
		select: function (event, ui) {
			$("user_search").value = ui.label
			get_user(ui.value)
		}
	});
});

