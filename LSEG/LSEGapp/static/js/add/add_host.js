/**
 * Created by ramyah on 04/08/2015.
 */

$(function(){

// Format the formset with those default values
    $('.role_formset').formset({
        extraClasses: ['row1'],
        added: function add_custom_function(formCount){   //totalForms = number of forms after adding the form

            var data = {};
            $('#id_form-' + (formCount -1) + '-role > option:not(:selected)').each(function(){  //populate data list with the first form dropdown without taking the selected item.
                role_id = $(this).val();
                role_name = $(this).text();
                data[role_id] = role_name;
            });
            $('#id_form-' + formCount + '-role').empty();       //populate the next form with data
            $.each(data, function(key, value){
                $('#id_form-' + formCount + '-role').append('<option value="' + key + '">' + value +'</option>');
            });


            if (Object.keys(data).length == 1){     //If size of the data array equal = 1 then we hide the add�
                $('.add-row').hide()
            }


        },

        pre_deletion: function pre_deletion_function(forms){
            if (forms.length == 1) {
                $('.formset').hide();
                $('#id_business_application')
                    .attr('disabled',false)
                    .val("");
                $('#add_host').attr('disabled',true)
            }
        }


    });



    $('.formset').hide();

    // ON BUSINESS APP CHANGE
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


    $('#add_host').click(function(){
        $('#id_business_application').attr('disabled',false);
        window.location.reload(true);
    });


});

