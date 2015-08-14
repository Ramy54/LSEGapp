/**
 * Created by ramyah on 04/08/2015.
 */

$(function(){


    $('.role_formset').formset({
        extraClasses: ['row1'
        ]
    });

    $('#id_business_application').attr('disabled',true);

    $('#id_business_application').change(function(){
        $('.formset').show();
        $('#add_host').attr('disabled',false);


        $(this).attr('disabled',true);

        var business_app = $(this).find(":selected").text(); // value of the selected business application in the dropdown
        if (business_app == "--SELECT--"){
            //TO DO
        }
        else{
            $.ajax({
                url: "/role_filter",
                type: "POST",
                data: {
                    business_app: business_app
                },
                dataType: "json",
                success: function(data) {
                    $('#id_form-0-role').empty();
                    $.each(data, function(key, value){

                        $('#id_form-0-role').append('<option value="' + key + '">' + value +'</option>');


                    });
                     var select_size = $('#id_form-0-role option').size();
                        if (select_size == 1){
                            $('.add-row').hide()
                        }

                }

            });



        }



    });



    $('#id_form-0-role').change(function(){
        $('#id_business_application').attr('disabled',true)
    });


    $('#save_host').click(function(){
        $('#id_business_application').attr('disabled',false);
        window.location.reload(true);
    });


});

