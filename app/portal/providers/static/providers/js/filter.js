/**
 * Filter State Object
 * a user is trying to pick a producer that matches their needs
 * @key @value
 * {
 *   facet: '',
 *   name: '',
 *   widget: '',
 *   options: {
 *      value: '',
 *      label: '',
 *      state: bool,
 *   }
 * }
 * Clear Selection
 * Don't send query if select
 * if over 5 alert user
 */

function populateFilterForms(filterArr) {
  var allFormsObj = document.forms;
  filterArr.forEach((filter, i) => {
    var facet = filter.facet;
    if (filter.visible) {
      if (filter.widget == 'compound-multiselect') {
        var options = [];
        for (var i = 0; i < filter.option_categories.length; i++) {
          opt_name = filter.option_categories[i][0];
          options.push(filter.options[opt_name]);
        }
      } else {
        var options = filter.options;
      }
      options.forEach((option, i) => {
        if (option.state == true) {
          document.querySelector(`input[name="${facet}"][value="${option.value}"]`).checked = true;
        }
      });
    }
  });
}

function updateFilterForms(filterDef) {
  // The code below is specific to the 'product_categories' and 'product_forms'
  // filters of the OH4S portal - we  wouldn't want (or know how) to do
  // this for every possible 'compound-multiselect' field. In the future, if
  // this is re-used, perhaps the 'filter' variable set in results_page.html
  // could track and define these relationships and be handled in a generic
  // way here...

  var filter_obj = JSON.parse(filterDef);
  var filter_update_fields = Object.keys(filter_obj);
  if (filter_update_fields.indexOf('product_categories') >= 0 && filter_obj['product_categories'].length > 0){
    // hide all product_form categories
    $('.compound-multiselect-category').hide();
    // loop through product_categories ids
    filter_obj['product_categories'].forEach((category_id, i) => {
      // show each corresponding product_form category
      $('#compound-multiselect-category-product_forms-'+category_id).show();
    });
  } else {
    $('.compound-multiselect-category').show();
  }

}

function populateFilterResults(arr) {
  const resultsCountElement = $('#results-count');
  resultsCountElement.html(arr.length.toString());
  const resultsWrap = document.getElementById('filter-results-wrap');
  if (arr.length < 1) {
    resultsWrap.innerHTML = '<h2>No results found</h2>';
    return;
  }
  resultsWrap.innerHTML = "";
  arr.forEach((provider, i) => {
    let providerUrl = `/producer/${provider.id}/`;
    let providerCard = providerToCard(provider, providerUrl);
    resultsWrap.insertAdjacentHTML('beforeend', providerCard);
    insertProductIcons(provider);
  });
}

$(document).ready(function() {

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
});

function showResultsSpinner() {
  // Add spinner to results section
  const resultsWrap = document.getElementById('filter-results-wrap');
  resultsWrap.innerHTML = `<div class="d-flex justify-content-end">
    <div class="spinner-border" role="status">
      <span class="visually-hidden">Loading...</span>
    </div>
  </div>`;
}

function filterQuery() {
  var filterReq = {};
  var allFormsObj = document.forms;
  var allFormsArr = document.querySelectorAll('form');
  allFormsArr.forEach((form, i) => {
    // Loop through add form elements
    for (var i = 0; i < form.elements.length; i++) {
      var option = form.elements.item(i);
      if (option.checked === true) {
        if (typeof(filterReq[form.name]) === "undefined") {
          filterReq[form.name] = [];
        }
        filterReq[form.name].push(option.value);
      }
    }
  });

  $.ajax('/providers/filter/', {
    type: 'POST',
    headers: {
      'X-CSRFToken': csrftoken
    },
    data: JSON.stringify(filterReq),
    success: function(response) {
      // needs work
      updateFilterForms(response[1]);
      populateFilterResults(response[0].providers);
    }
  });
}

/**
 * Create HTML with class card fromn array
 * @type {[function]}
 */
const providerToCard = (provider, providerUrl) => {
  const cardElement = `<div class="col" id="results-card-${provider.id}">` +
      `<a class="card h-100" href="${providerUrl}">` +
        `<div class="card-body">` +
          `<h5 class="card=title">${provider.name}</h5>` +
          `<p>${provider.businessAddressCity}, ${provider.businessAddressState.initialism}</p>` +
          `<div class='producer-products'></div>` +
        `</div>` +
      `</a>` +
    `</div>`;
  return cardElement;
}

/**
 * Insert html into results provider card: images of product categories
 * @type {[function]}
 */
const insertProductIcons = (provider) => {
  const imgWidth = 30;
  const imgMargin = 10;
  var providerCard = $(`#results-card-${provider.id}`);
  var productImgDiv = providerCard.find('.producer-products').first();
  var remainingCategoryCount = provider.product_categories.length;
  var maxImgShown = parseInt(productImgDiv.width()/(imgWidth+imgMargin)) - 2;
  var extraCategories = remainingCategoryCount - maxImgShown;
  provider.product_categories.forEach((category, i) => {
    if (i < maxImgShown) {
        productImgDiv.append(`<img class="producer-product-image" src="${category.image}" style="width: ${imgWidth}px; margin-right: ${imgMargin}px"/>`);
    }
  });
  if (extraCategories > 0) {
    productImgDiv.append(`<span class="extra-products-count">+${extraCategories}</span>`);
  }
}



/**
 * Get CSRF cookie
 */

 function getCookie(name) {
     let cookieValue = null;
     if (document.cookie && document.cookie !== '') {
         const cookies = document.cookie.split(';');
         for (let i = 0; i < cookies.length; i++) {
             const cookie = cookies[i].trim();
             // Does this cookie string begin with the name we want?
             if (cookie.substring(0, name.length + 1) === (name + '=')) {
                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                 break;
             }
         }
     }
     return cookieValue;
 }
 const csrftoken = getCookie('csrftoken');

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
