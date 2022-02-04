$(function() {
  'use strict';

  $.validator.setDefaults({
    submitHandler: function() {
      alert("submitted!");
    }
  });
  $(function() {
    // validate login form on keyup and submit
    $("#loginModalForm").validate({
      rules: {
        loginNumberPhone: {
          required: true,
          checkMaskPhone: true

        },
        loginPassword: {
          required: true,
          minlength: 8
        }
      },
      messages: {
        loginNumberPhone: {
          required: "Пожалуйста, введите номер телефона",
          checkMaskPhone: "Пожалуйста, введите правильный номер телефона",
          minlength: "Пожалуйста, введите правильный номер телефона"
        },
        loginPassword: {
          required: "Пожалуйста, введите пароль",
          minlength: "Ваш пароль должен быть не менее 8 символов"
        }
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
        signUpNameCompany: {
          required: true
        },
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
          equalTo: "#signUpPassword"
        },


      },
      messages: {
        signUpNameCompany: {
          required: "Пожалуйста, введите название компании"
        },
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
  $(function() {
    // validate signup form on keyup and submit
    $("#forgotPasswordModalForm").validate({
      rules: {
        forgotPasswordNumberPhone: {
          required: true,
          checkMaskPhone: true
        }
      },
      messages: {
        forgotPasswordNumberPhone: {
          required: "Пожалуйста, введите номер телефона",
          checkMaskPhone: "Пожалуйста, введите правильный номер телефона",
          minlength: "Пожалуйста, введите правильный номер телефона"
        }
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