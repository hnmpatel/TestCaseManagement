$(document).ready(function(){
    $('#table_testcase').dataTable();
});

$(window).load(function(){
	load_categories();
});

// To load all categories for a particular project which is selected in select tag
function load_categories(){
	$.ajax({
		type: "POST",
			url : "/testcase/load_category/",
			data : {
				'p_name' : $("#project").val(),
				'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
			},
			success : render_categories,
			dataType : "html"
	});
}

function render_categories(data, textStatus, jqXHR)
{
	$('#category').html(data);
	load_testcases();
}

function load_testcases(){
	$.ajax({
		type: "POST",
			url : "/testcase/load_testcases/",
			data : {
				'p_name' : $("#project").val(),
				'c_name' : $("#category").val(),
				'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
			},
			success : render_testcases,
			dataType : "html"
	});
}

function render_testcases(data, textStatus, jqXHR)
{
	$('#tc_list').html(data);
}
