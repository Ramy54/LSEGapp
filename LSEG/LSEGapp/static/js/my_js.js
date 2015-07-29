/**
 * Created by ramyah on 29/07/2015.
 */


$(function(){
    $(".variable").click(function(){
        var component_var_id = this.id;
        var old_value = $(".variable[id='" + component_var_id + "']").text();
        var new_value = prompt("Enter value",old_value);

        $.ajax({
            url: "/edit_value",
            type: "POST",
            data: {
                new_value: new_value,
                component_var_id: component_var_id
            },
            success: function () {
                $(".variable[id='" + component_var_id + "']").text(new_value);
            }

        })
    })

    $(".variable_template").click(function(){
        var var_id = this.id;
        var old_value = $(".variable_template[id='" + var_id + "']").text();
        var new_value = prompt("Enter value",old_value);

        $.ajax({
            url: "/edit_default_value",
            type: "POST",
            data: {
                new_value: new_value,
                var_id: var_id
            },
            success: function () {
                $(".variable_template[id='" + var_id + "']").text(new_value);
            }

        })
    })

})