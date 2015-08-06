/**
 * Created by ramyah on 04/08/2015.
 */

$(function(){

    $('.formset').formset({
        extraClasses: ['row1']
    });


    $('#id_business_application').change(function(){
        var business_app = $(this).find(":selected").text(); // value of the selected business application in the dropdown

        $.ajax({
            url: "/autocompletion_role_name",
            type: "POST",
            data: {
                business_app: business_app
            },
            dataType: "json",
            success: function(data) {
                $('#id_name')
                    .val(data.prefix)
                    .keyup(function(){
                        var prefix = data.prefix;
                        if (!(this.value.match('^' + prefix + ''))){
                            this.value = '' + prefix;
                        }
                    });
            }

        })
    });

    $(".delete_fade_out").fadeOut(3000,function(){

    });

});