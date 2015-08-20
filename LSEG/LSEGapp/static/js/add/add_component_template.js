/**
 * Created by ramyah on 20/08/2015.
 */

$(function(){

    $('.formset').formset({
        extraClasses: ['row1'],

        added: function add_custom_function(formCount){   //totalForms = number of forms after adding the form

            var data = {};
            $('#id_form-' + (formCount -1) + '-variable > option:not(:selected)').each(function(){  //populate data list with the first form dropdown without taking the selected item.
                component_id = $(this).val();
                component_name = $(this).text();
                data[component_id] = component_name;
            });

            $('#id_form-' + formCount + '-variable').empty();       //populate the next form with data
            $.each(data, function(key, value){
                $('#id_form-' + formCount + '-variable').append('<option value="' + key + '">' + value +'</option>');
            });


            if (Object.keys(data).length == 1){     //If size of the data array equal = 1 then we hide the addè
                $('.add-row').hide()
            }
        }
    });





});