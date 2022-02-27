$(function() {
  'use strict';

  $(function() {
    $('#dataTableMyQuestionnaire').DataTable({
      "lengthChange": false,
      "aLengthMenu": false,
      "iDisplayLength": 10,
      "paging": false,
      "language": {
        "url": "//cdn.datatables.net/plug-ins/1.11.4/i18n/ru.json",
        search: ""
      }
    });
    $('#dataTableMyQuestionnaire').each(function() {
      var datatable = $(this);
      // SEARCH - Add the placeholder for Search and Turn this into in-line form control
      var search_input = datatable.closest('.dataTables_wrapper').find('div[id$=_filter] input');
      search_input.attr('placeholder', 'Search');
      search_input.removeClass('form-control-sm');
      // LENGTH - Inline-Form control
      var length_sel = datatable.closest('.dataTables_wrapper').find('div[id$=_length] select');
      length_sel.removeClass('form-control-sm');
    });
  });

  $(function() {
    $('#dataTableMyVacancy').DataTable({
      "lengthChange": false,
      "aLengthMenu": false,
      "iDisplayLength": 10,
      "paging": false,
      "language": {
        "url": "//cdn.datatables.net/plug-ins/1.11.4/i18n/ru.json",
        search: ""
      }
    });
    $('#dataTableMyVacancy').each(function() {
      var datatable = $(this);
      // SEARCH - Add the placeholder for Search and Turn this into in-line form control
      var search_input = datatable.closest('.dataTables_wrapper').find('div[id$=_filter] input');
      search_input.attr('placeholder', 'Search');
      search_input.removeClass('form-control-sm');
      // LENGTH - Inline-Form control
      var length_sel = datatable.closest('.dataTables_wrapper').find('div[id$=_length] select');
      length_sel.removeClass('form-control-sm');
    });
  });

});