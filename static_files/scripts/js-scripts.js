$(document).ready(function () {
	$(".heart").bind("click", function (event) {
		$(this).first().removeClass("far");
		$(this).first().addClass("fas");
	});
});
