$(function() {
  'use strict';

  $.validator.setDefaults({
    
  });
  $(function() {
    // validate login form on keyup and submit
    $("#loginModalForm").validate({
      rules: {
        loginNumberPhone: {
          required: true,

        },
        loginPassword: {
          required: true,
          minlength: 8
        }
      },
      messages: {
        loginNumberPhone: {
          required: "Пожалуйста, введите номер телефона",
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
        $(element).addClass('is-invalid');
      },
      unhighlight: function(element, errorClass) {
            $(element).removeClass("is-invalid").addClass('is-valid');
        },
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
          validatePhoneUser: true
        },
        signUpEmail: {
          required: true,
          email: true,
          validateEmailUser: true
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
        signUpConfirmKey: {
          required: true,
          number: true,
          minlength: 4
        },


      },
      messages: {
        signUpNameCompany: {
          required: "Пожалуйста, введите название компании"
        },
        signUpNumberPhone: {
          required: "Пожалуйста, введите номер телефона",
          checkMaskPhone: "Пожалуйста, введите правильный номер телефона",
          validatePhoneUser: "Пользователь с таким номером телефона уже зарегестрирован",
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
        signUpConfirmKey: {
          required: "Пожалуйста, введите код подтверждения",
          number: "Код подтверждения должен состоять из 4 символов",
          minlength: "Код подтверждения должен состоять из 4 символов"
        },
        signUpEmail: {
          required: "Пожалуйста, введите адрес электронной почты",
          email:"Пожалуйста, введите действительный адрес электронной почты",
          validateEmailUser:"Пользователь с таким адресом электронной почтой уже зарегестрирован"
        }
      },
      errorPlacement: function(label, element) {
        label.addClass('mt-2 text-danger');
        label.insertAfter(element);
      },
      highlight: function(element, errorClass) {
        $(element).addClass('is-invalid');
      },
      unhighlight: function(element, errorClass) {
            $(element).removeClass("is-invalid").addClass('is-valid');
        },
    });
  });
  $(function() {
    // validate signup form on keyup and submit
    $("#forgotPasswordModalForm").validate({
      rules: {
        forgotPasswordEmail: {
          required: true,
          email: true
        },
        forgotPasswordPassword: {
          required: true,
          minlength: 8
        },
        forgotPasswordConfirmPassword: {
          required: true,
          minlength: 8,
          equalTo: "#forgotPasswordPassword"
        },
        forgotPasswordConfirmKey: {
          required: true,
          number: true,
          minlength: 4
        },
      },
      messages: {

        signUpEmail: {
          required: "Пожалуйста, введите адрес электронной почты",
          email:"Пожалуйста, введите действительный адрес электронной почты"
        },
        forgotPasswordPassword: {
          required: "Пожалуйста, введите пароль",
          minlength: "Ваш пароль должен быть не менее 8 символов"
        },
        forgotPasswordConfirmPassword: {
          required: "Пожалуйста, введите пароль",
          minlength: "Ваш пароль должен быть не менее 8 символов",
          equalTo: "Пожалуйста, введите тот же пароль, что и выше"
        },
        forgotPasswordConfirmKey: {
          required: "Пожалуйста, введите код подтверждения",
          number: "Код подтверждения должен состоять из 4 символов",
          minlength: "Код подтверждения должен состоять из 4 символов"
        },
      },
      errorPlacement: function(label, element) {
        label.addClass('mt-2 text-danger');
        label.insertAfter(element);
      },
      highlight: function(element, errorClass) {
        $(element).addClass('is-invalid');
      },
      unhighlight: function(element, errorClass) {
            $(element).removeClass("is-invalid").addClass('is-valid');
        },
    });
  });
});