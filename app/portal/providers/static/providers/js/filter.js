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
      filter.options.forEach((option, i) => {
        if (option.state == true) {
          document.querySelector(`input[name="${facet}"][value="${option.value}"]`).checked = true;
        }
      });
    }
  });
}

function populateFilterResults(arr) {
  const resultsCountElement = document.getElementById('results-count');
  resultsCountElement.innerHTML = arr.length.toString();
  const resultsWrap = document.getElementById('filter-results-wrap');
  if (arr.length < 1) {
    resultsWrap.innerHTML = '<h2>No results found</h2>';
    return;
  }
  resultsWrap.innerHTML = "";
  arr.forEach((provider, i) => {
    let providerUrl = `/providers/provider/${provider.id}/`;
    let addCol = true;
    let providerCard = providerToCard(provider.name, providerUrl, addCol);
    resultsWrap.insertAdjacentHTML('beforeend', providerCard);
  });
}

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
      populateFilterForms([response[1]]);
      populateFilterResults(response[0].providers);
    }
  });
}

/**
 * Create HTML with class card fromn array
 * @type {[function]}
 */
const providerToCard = (name, providerUrl) => {
  const cardElement = `<div class="col"><a class="card h-100" href="${providerUrl}"><div class="card-body"><h5 class="card=title">${name}</h5></div></a></div>`;
  return cardElement;
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
