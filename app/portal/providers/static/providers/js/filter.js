/**
 * Filter State Object
 * a user is trying to pick a producer that matches their needs
 * @key @value
 * {
 *   'selfIdentification': [],
 *   'county': [],
 *   'deliveryMethod': [],
 *   'usdaComponents': [],
 *   'productType': [],
 *   'productionPractices': [],
 *   'distributors': [],
 * }
 * {
 *   'facite': <unique_id>
 *   'name':
 *   'options': {
 *      <id>: '',
 *      <label>: '',
 *      <checked>: bool,
 *   }
 * }
 * Clear Selection
 * Don't send query if select
 * if over 5 alert user
 */

const filterData = JSON.parse(document.getElementById('filters-data').textContent);

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

function loadJson(selector) {
  return JSON.parse(document.querySelector(selector).getAttribute('data-json'));
}

function filterQuery(filters) {

  var forms = document.querySelectorAll('form');

  for (var i = 0; i < forms.length; i++) {
    var form = forms[i];
    var formName = form.name;
    // get form inputs that are checked
    console.log(formName);
  }

  // for each form with checked boxes
    // key = facet
    // value = filter form input field value

    /*
    {
     'product_categories': [ 3, 7, 26],
     'identities': [ 9, 43, 82],
     ...
      }
     */

  // build a query that filters producers using the above structure

}

/**
 * Form Validation
 * ([event])
 */
// (function () {
//   'use strict'
//
//   // Fetch all the forms we want to apply custom Bootstrap validation styles to
//   var forms = document.querySelectorAll('.needs-validation')
//
//   // Loop over them and prevent submission
//   Array.prototype.slice.call(forms)
//     .forEach(function (form) {
//       form.addEventListener('submit', function (event) {
//         if (!form.checkValidity()) {
//           event.preventDefault()
//           event.stopPropagation()
//         }
//
//         form.classList.add('was-validated')
//       }, false)
//     })
// })()
