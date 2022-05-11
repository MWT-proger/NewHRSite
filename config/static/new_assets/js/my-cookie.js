$(function() {
  // Проверяем запись в куках о посещении
  // Если запись есть - ничего не происходит
     if (!$.cookie('hideModal')) {
  // если cookie не установлено появится окно
  // с задержкой 5 секунд

      setTimeout("$('#button_cookies').click();", 2000);
}
     $.cookie('hideModal', true, {
   // Время хранения cookie в днях
	expires: 1,
	path: '/'
   });
});