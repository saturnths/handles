var $input = $('#new-url-input');

$('#add-url').on('click', function() {
  $('#list').show();
  $('#submit').removeAttr('disabled');
  var item =  '<li class="list-group-item">' +
              '<div class="row-data">' +
              $input.val() +
              '</div>' +
              '<button type="button" class="btn btn-xs btn-danger pull-right remove-url">' +
              '<span class="glyphicon glyphicon-remove" aria-hidden="true"></span>' +
              '</button>' +
              '</li>';
  $('#urls').append(item);
  $input.val('');
});

$('body').on('click', '.remove-url', function(e) {
  $(e.target).closest('.list-group-item').remove();
});

$('#submit').on('click', function() {
  var urls = [];
  $('#urls .row-data').each(function() {
    urls.push($(this).text());
  });

  $.ajax({
    url: '/api/search',
    type: "POST",
    data: JSON.stringify({
      "mode": $("input[type='radio']:checked").val(),
      "urls": urls
    }),
    contentType: "application/json",
    dataType: "json"
  })
  .done(function(data) {
    $('#results-container').show();
    $('#results').empty();

    data.forEach(function(page) {
      var rows = '';
      page.results.forEach(function(result) {
        rows += '<p>' + result + '</p>';
      });

      if (rows.length === 0) { rows = '<p>No results.</p>'; }
      $('#results').append('<h3>' + page.url + '</h3>' + rows);
    });
  });
});
