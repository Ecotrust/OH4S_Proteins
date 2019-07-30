$('#filter-form').submit(function(event) {
  event.preventDefault();
});

$('#filter-form').on(
  'change',
  function() {
    if (category_id != null) {
      var url = "/providers/filter_providers/" + category_id + "/";
    } else {
      var url = "/providers/filter_providers/";
    }
    // Fire off AJAX request to backend to run filter.
    //    Callback takes HTML results and replaces $('#product-results-list') content
    var filter_request = $.post(url, $('#filter-form').serialize() )
      .done(function( data ) {
        $('#product-results-list').html(data);
        try {
          $("#provider-count").html($('#product-results-list').children().length);
        } catch (error) {
          console.log(error);
        }
      });
  }
);
