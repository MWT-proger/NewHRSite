$(function() {
  'use strict';

  $.validator.setDefaults({
    submitHandler: function() {
      alert("submitted!");
    }
  });
  $(function() {
    // validate signup form on keyup and submit
    $("#loginModalForm").validate({
      rules: {
        loginNumberPhone: {
          required: true

        },
        loginPassword: {
          required: true,
          minlength: 8
        },
        // confirm_password: {
        //   required: true,
        //   minlength: 8,
        //   equalTo: "#password"
        // },
      },
      messages: {
        loginNumberPhone: {
          required: "Пожалуйста, введите номер телефона",
          minlength: "Пожалуйста, введите правильный номер телефона"
        },
        loginPassword: {
          required: "Пожалуйста, введите пароль",
          minlength: "Ваш пароль должен быть не менее 8 символов"
        },
        // confirm_password: {
        //   required: "Пожалуйста, введите пароль",
        //   minlength: "Ваш пароль должен быть не менее 8 символов",
        //   equalTo: "Пожалуйста, введите тот же пароль, что и выше"
        // }
      },
      errorPlacement: function(label, element) {
        label.addClass('mt-2 text-danger');
        label.insertAfter(element);
      },
      highlight: function(element, errorClass) {
        $(element).parent().addClass('has-danger');
        $(element).addClass('form-control-danger');
      }
    });
  });
  $(function() {
    // validate signup form on keyup and submit
    $("#signUpModalForm").validate({
      rules: {
        signUpNumberPhone: {
          required: true,
          checkMaskPhone: true
        },
        signUpEmail: {
          required: true,
          email: true
        },
        signUpPassword: {
          required: true,
          minlength: 8
        },
        signUpConfirmPassword: {
          required: true,
          minlength: 8,
          equalTo: "#password"
        },


      },
      messages: {
        signUpNumberPhone: {
          required: "Пожалуйста, введите номер телефона",
          checkMaskPhone: "Пожалуйста, введите правильный номер телефона",
          minlength: "Пожалуйста, введите правильный номер телефона"
        },
        signUpPassword: {
          required: "Пожалуйста, введите пароль",
          minlength: "Ваш пароль должен быть не менее 8 символов"
        },
        signUpConfirmPassword: {
          required: "Пожалуйста, введите пароль",
          minlength: "Ваш пароль должен быть не менее 8 символов",
          equalTo: "Пожалуйста, введите тот же пароль, что и выше"
        },
        signUpEmail: "Пожалуйста, введите действительный адрес электронной почты",
      },
      errorPlacement: function(label, element) {
        label.addClass('mt-2 text-danger');
        label.insertAfter(element);
      },
      highlight: function(element, errorClass) {
        $(element).parent().addClass('has-danger');
        $(element).addClass('form-control-danger');
      }
    });
  });
});