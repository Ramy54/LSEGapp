/**
 * Created by ramyah on 04/08/2015.
 */

$(function(){

    $('.role_formset').formset({
        extraClasses: ['row1']
    });


    $('#id_business_application').change(function(){
        var business_app = $(this).find(":selected").text(); // value of the selected business application in the dropdown

        $.ajax({
            url: "/role_filter",
            type: "POST",
            data: {
                business_app: business_app
            },
            dataType: "json",
            success: function(data) {
                $('select[name*=form-]').empty();
                $.each(data, function(key, value){

                    $('select[name*=form-]').append('<option value="' + key + '">' + value +'</option>');

                })
            }

        })
    });

});