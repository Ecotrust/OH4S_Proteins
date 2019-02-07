$('#filter-form').submit(function(event) {
  event.preventDefault();
});

$('#filter-form').on(
  'change',
  function() {
    var url = "/providers/filter_products/" + category_id + "/";
    // Fire off AJAX request to backend to run filter.
    //    Callback takes HTML results and replaces $('#product-results-list') content
    var filter_request = $.post(url, $('#filter-form').serialize() )
      .done(function( data ) {
        $('#product-results-list').html(data);
      });
  }
);
