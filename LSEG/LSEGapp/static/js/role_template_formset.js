/**
 * Created by ramyah on 04/08/2015.
 */

$(function(){

    $('.formset').formset({
        extraClasses: ['row1']
    });


    $('#id_business_application').change(function(){
        var business_app = $(this).find(":selected").text(); // value of the selected business application in the dropdown
        prefix ='';

        $.ajax({
            url: "/autocomplete_role_name",
            type: "POST",
            data: {
                business_app: business_app
            },
            dataType: "json",
            success: function(data) {
                prefix = data.prefix;
                $('#id_name')
                    .val(prefix)
                    .keyup(function(){
                        if (!(this.value.match('^' + prefix + ''))){
                            this.value = '' + prefix;
                        }
                    });
            }



        });



    });


});