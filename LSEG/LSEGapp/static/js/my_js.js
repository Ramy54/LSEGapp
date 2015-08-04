/**
 * Created by ramyah on 29/07/2015.
 */


$(function() {
    $(".variable").dblclick(function () {
        var element = this;
        var component_var_id = element.id;
        var old_value = $(".variable[id='" + component_var_id + "']").text();

        $(element).html('<input style="width:100%" class="val_input" type="text" value="' + old_value + '" />');

        $(".val_input")
            .focus()
            .keyup(function(event){
                new_value = $(this).val();
                if(event.keyCode == 13 && new_value != "" ){
                    $(element).html($(".val_input").val().trim());
                    $.ajax({
                        url: "/edit_value",
                        type: "POST",
                        data: {
                            new_value:new_value,
                            component_var_id:component_var_id
                        },
                        success: function () {
                            $(".variable[id='" + component_var_id + "']").text(new_value);
                        }
                    })
                }
            });


    });

    $(".variable_template").dblclick(function () {
        var element = this;
        var var_id = element.id;
        var old_value = $(".variable_template[id='" + var_id + "']").text();

        $(element).html('<input style="width:100%" class="val_input" type="text" value="' + old_value + '" />');

        $(".val_input")
            .focus()
            .keyup(function(event){
                new_value = $(this).val();
                if(event.keyCode == 13 && new_value != "" ){
                    $(element).html($(".val_input").val().trim());
                    $.ajax({
                        url: "/edit_default_value",
                        type: "POST",
                        data: {
                            new_value: new_value,
                            var_id: var_id
                        },
                        success: function () {
                        }
                    })
                }
            });
    });



    $("button[name=old_value]").click(function () {
        var component_var_id = this.id;

        var boolean = confirm("Are you sure you want to set default value?");

        if (boolean==true)
            $.ajax({
                url: "/set_default",
                type: "POST",
                data: {
                    component_var_id: component_var_id
                },
                dataType: "json",
                success: function(data) {
                    $(".variable[id='" + component_var_id + "']").text(data.old_value);
                }

            })
    });


});