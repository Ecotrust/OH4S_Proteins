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
    $('#home-filter-button').html(browse_all_default);
  } else {
    $('#home-filter-button').html(browse_filtered_default);
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

var get_filter_form = function() {
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
  return form;
}

var go_to_product_results = function(product_id, product_name) {
  var form = get_filter_form();
  var label = `<label class="list-group-item">
    <input class="form-check-input me-1" name="product_categories" type="checkbox" value="${product_id}" checked>" ${product_name}"</label>`;
  form.append(label);
  form.appendTo('body').submit();
}

var go_to_results = function() {
  var form = get_filter_form();
  form.appendTo('body').submit();

}
