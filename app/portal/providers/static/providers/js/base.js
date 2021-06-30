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
	});

	var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
	var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
	  return new bootstrap.Tooltip(tooltipTriggerEl)
	});

	document.querySelectorAll('.expandable-wrap').forEach((el, i) => {
		el.addEventListener('click', function(event) {
			el.classList.toggle('show');
			el.querySelector('.expandable').classList.toggle('show');
		});
	});

	document.querySelectorAll('.expandable').forEach((el, i) => {
		if (el.offsetHeight > 72) {
			el.classList.remove('show');
			el.closest('.expandable-wrap').classList.add('has-expand');
		}
	});
});
