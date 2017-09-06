/**
 * Created by hbot on 7/8/17.
 */
var Gate = {
    signUpValidation: function () {
        $('#sign_up').validate({
            rules: {
                // 'terms': {
                //     required: true
                // },
                'confirm_password': {
                    equalTo: '[name="password"]'
                },
                'master_password': {
                    notEqual: '[name="password"]'
                }
            },
            messages:{
                master_password:{
                    notEqual: "Password and master password can't be same!!!!"
                }
            },
            highlight: function (input) {
                //console.log(input);
                $(input).parents('.form-line').addClass('error');
            },
            unhighlight: function (input) {
                $(input).parents('.form-line').removeClass('error');
            },
            errorPlacement: function (error, element) {
                $(element).parents('.input-group').append(error);
                $(element).parents('.form-group').append(error);
            }
        });
    },
    unlockFormValidate: function () {
        $('#unlock').validate({
            highlight: function (input) {
                //console.log(input);
                $(input).parents('.form-line').addClass('error');
            },
            unhighlight: function (input) {
                $(input).parents('.form-line').removeClass('error');
            },
            errorPlacement: function (error, element) {
                $(element).parents('.input-group').append(error);
                $(element).parents('.form-group').append(error);
            }
        });
    },
    signInValidation: function () {
        $('#sign_in').validate({
            highlight: function (input) {
                //console.log(input);
                $(input).parents('.form-line').addClass('error');
            },
            unhighlight: function (input) {
                $(input).parents('.form-line').removeClass('error');
            },
            errorPlacement: function (error, element) {
                $(element).parents('.input-group').append(error);
            }
        });
    },
    forgotPasswordValidation: function () {
        $('#sign_in').validate({
            highlight: function (input) {
                //console.log(input);
                $(input).parents('.form-line').addClass('error');
            },
            unhighlight: function (input) {
                $(input).parents('.form-line').removeClass('error');
            },
            errorPlacement: function (error, element) {
                $(element).parents('.input-group').append(error);
            }
        });
    },
    ledgerHeadValidation: function () {
        $('#add_ledger_head').validate({
            rules: {

            },
            highlight: function (input) {
                $(input).parents('.form-line').addClass('error');
            },
            unhighlight: function (input) {
                $(input).parents('.form-line').removeClass('error');
            },
            errorPlacement: function (error, element) {
                $(element).parents('.form-group').append(error);
            }
        });
    },
    editledgerHeadValidation: function () {
        $('#edit_ledger_head').validate({
            rules: {

            },
            highlight: function (input) {
                $(input).parents('.form-line').addClass('error');
            },
            unhighlight: function (input) {
                $(input).parents('.form-line').removeClass('error');
            },
            errorPlacement: function (error, element) {
                $(element).parents('.form-group').append(error);
            }
        });
    },
    headEditHandler: function () {
        $('.btnEdit').click(function (e) {
            e.preventDefault();
            // console.log('i am in fire');
            var dataId = $(this).attr('data-id');
            var ledgerCode = $(this).attr('data-ledger-code');
            var headName = $(this).siblings('p').text();

            $('#acc_head_name').val(headName);
            $('#acc_head_id').val(dataId);
            $('#acc_ledger_code').val(ledgerCode);

            $('#editHeadModal').modal('show');

        });

        $('#edit_ledger_head').submit(function (e) {
            e.preventDefault();
            var data = $(this).serialize();
            var postURL = $(this).attr('action')

            $.post(postURL,data,function(res, status){
                if(status==="success"){
                    if(res.success){
                        showNotification("bg-teal", res.message, 'top', 'right', 'animated zoomInRight', 'animated zoomOutRight');
                        $('#editHeadModal').modal('hide');
                        setTimeout(function () {
                            location.reload();

                        },2000);
                    }
                    else{
                        showNotification("bg-red", res.message, 'top', 'right', 'animated zoomInRight', 'animated zoomOutRight');
                    }
                }
                else{
                    console.log(res);
                    console.log(status);
                }

            });

        });
    },
    voucherFormValidate: function () {
        $('#add_voucher').validate({
            rules: {
                'description':{
                    maxlength: 500
                }
            },
            highlight: function (input) {
                $(input).parents('.form-line').addClass('error');
            },
            unhighlight: function (input) {
                $(input).parents('.form-line').removeClass('error');
            },
            errorPlacement: function (error, element) {
                $(element).parents('.form-group').append(error);
            }
        });
        $('#add_voucher').submit(function (e) {
            e.preventDefault();
            if(Voucher.payment_method_table_count){
                this.submit();
            }
            else{
                showNotification("bg-red", 'Please add payment method!', 'top', 'right', 'animated zoomInRight', 'animated zoomOutRight');
            }
        });
    },
    accVoucherFormValidate: function () {
        $('#add_acc_voucher').validate({
            rules: {
                'description':{
                    maxlength: 500
                }
            },
            highlight: function (input) {
                $(input).parents('.form-line').addClass('error');
            },
            unhighlight: function (input) {
                $(input).parents('.form-line').removeClass('error');
            },
            errorPlacement: function (error, element) {
                $(element).parents('.form-group').append(error);
            }
        });

    },
};