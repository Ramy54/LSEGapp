
$(function() {

    var variable_id =


        $(".variable").dblclick(function () {
            var element = this;
            var component_var_id = element.id;
            var old_value = $(".variable[id='" + component_var_id + "']").text();

            $(element).html('<input style="width:85%" class="val_input" type="text" value="' + old_value + '" />');

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

    $(".delete_fade_out").fadeOut(3000,function(){

    });




    $("#jsGrid").jsGrid({

        width: "100%",
        pageSize: 15,
        pageButtonCount: 5,
        filtering:true,
        inserting:true,
        autoload:true,
        editing: true,

        onItemDeleting: function(grid){
            var deferred = $.Deferred();

            $.ajax({
                url: '/is_var_used',
                type: "POST",
                dataType: 'json',
                data: {'id':grid.item.id},
                success: function(data){
                    alert(data.boolean)
                    deferred.resolve(data.boolean);
                }
            });

            return deferred.promise();
        },



        fields: [
            { name: "name", title: "Name", type: "text", align: "center"},
            { name: "type", title: "Type", type: "text", align: "center"},
            { name: "default_value", title: "Default Value", type: "text", align: "center", filtering:false},
            { name: "required", title: "Required", type: "checkbox", align: "center", filtering: false},
            { name: "description", title: "Description", type: "text", align: "center", filtering:false },
            { type: "control"}
        ],

        controller:{
            loadData: function(filter) {
                name_filter = filter.name;
                type_filter = filter.type;
                var deferred = $.Deferred();

                $.ajax({
                    url: '/get_vars',
                    type: "POST",
                    dataType: 'json',
                    data: {"name_filter":name_filter, "type_filter":type_filter},
                    success: function(data){
                        deferred.resolve(data.variable);
                    }
                });

                return deferred.promise();
            },

            insertItem: function(item) {
                var name = item.name;
                var type = item.type;
                var default_value = item.default_value;
                var required = item.required;
                var description = item.description;

                $.ajax({
                    type: "POST",
                    url: "/add_variable",
                    data: {"name":name, "type":type, "default_value":default_value, "required" :required, "description": description},
                    dataType: "json",
                    success: function(data){
                        if (data.error_mesage){
                            $('.alert_red').text(data.error_mesage).fadeOut(3000)
                        }
                        else{
                            $('.alert_green').text(data.add_message).fadeOut(3000)
                        }

                    }
                });
            },

            updateItem: function(item) {
                var id = item.id;
                var name = item.name;
                var type = item.type;
                var default_value = item.default_value;
                var required = item.required;
                var description = item.description;
                $.ajax({
                    type: "POST",
                    url: "/update_variable",
                    data: {"id":id, "name":name, "type":type, "default_value":default_value, "required" :required, "description": description},
                    dataType: "json"
                });

            },

            deleteItem: function(item) {
                var var_name = item.name;

                return $.ajax({
                    type: "POST",
                    url: "/delete_variable",
                    dataType: "json",
                    data: {'var_name':var_name},
                    success: function(data){
                        $('.alert_red').text(data.message).fadeOut(3000)
                    }

                });
            }
        }

    });



});