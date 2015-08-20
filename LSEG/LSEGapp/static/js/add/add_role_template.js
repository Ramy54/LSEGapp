/**
 * Created by ramyah on 04/08/2015.
 */

$(function(){

    $('.formset').formset({
        extraClasses: ['row1'],

        added: function add_custom_function(formCount){   //totalForms = number of forms after adding the form

            var data = {};
            $('#id_form-' + (formCount -1) + '-component > option:not(:selected)').each(function(){  //populate data list with the first form dropdown without taking the selected item.
                component_id = $(this).val();
                component_name = $(this).text();
                data[component_id] = component_name;
            });

            $('#id_form-' + formCount + '-component').empty();       //populate the next form with data
            $.each(data, function(key, value){
                $('#id_form-' + formCount + '-component').append('<option value="' + key + '">' + value +'</option>');
            });


            if (Object.keys(data).length == 1){     //If size of the data array equal = 1 then we hide the addè
                $('.add-row').hide()
            }
        }
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