$(document).ready(function() {
	$('.modal-footer').find('.btn-clear').on('click', function(e) {
		e.preventDefault();
		let $checked = $('.modal.show form input:checked')
		if ($checked.length > 0) {
			for (var i = 0; i < $checked.length; i++) {
				$checked[i].checked = false;
			}
		}
	});

	$('.modal-footer').find('.btn-apply').on('click', function(e) {
		let $checked = $('.modal.show form input:checked')
		if ($checked.length > 0) {
			
		}
	})
});