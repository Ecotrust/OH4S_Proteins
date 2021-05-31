$(document).ready(function(){
  $("form.home-filter-form").change(function(){
    toggle_home_filter($(this));
  });
});

var filters = {};
// Observing changes to filters following Elliot B.'s advice:
//  https://stackoverflow.com/a/50862441/706797
var filterProxy = new Proxy(filters, {
  set: function(target, key, value) {
    target[key] = value;
    reset_filter_button();
    return true;
  }
});

var reset_filter_button = function() {
  keys = Object.keys(filters);
  filter_all = true;
  for (var i = 0; i < keys.length; i++) {
    key = keys[i];
    if (filters[key].length > 0) {
      filter_all = false;
      break;
    }
  }
  if (filter_all) {
    $('#home-filter-button').html('Browse All Providers &gt;&gt;');
  } else {
    $('#home-filter-button').html('See Filtered Providers &gt;&gt;');
  }
}

var toggle_home_filter = function(form) {
  var checked = [];
  var inputs = form.find('input');
  for (var i = 0; i < inputs.length; i++) {
    input = inputs[i];
    if (input.checked) {
      checked.push(parseInt(input.value));
    }
  }
  filterProxy[form.attr('name')] = checked;
}

var go_to_results = function() {
  var form = $('<form id="final-home-filter-form"></form>');
  form.attr("method", "post");
  form.attr("action", "/results/");
  $.each( $('form.home-filter-form'), function(filter_index) {
    var labels = $(this).find('label');
    for (var i = 0; i < labels.length; i++) {
      label = labels[i];
      form.append(label);
    }

  });
  form.appendTo('body').submit();

}