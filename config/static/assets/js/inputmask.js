(function($) {
  'use strict';

  // initializing inputmask
  $(":input").inputmask(
      {definitions: {
        '0': "[0-9]",
        'a': "[A-Za-z]",
        '*': "[A-Za-z0-9]"
    },}
  );

})(jQuery);