
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


    $("#jsGrid").jsGrid({

        width: "100%",
        pageSize: 15,
        pageButtonCount: 5,
        filtering:true,
        inserting:true,
        autoload:true,
        editing: true,

        onItemDeleting: function(grid){ //Return if a variable is used by other components
            $.ajax({
                url: '/is_var_used',
                type: "POST",
                dataType: 'json',
                async:false,
                data: {'name':grid.item.name},
                success: function(data){
                    used = data.boolean;
                    message = data.message;
                    $('.alert_red').text(message).show().fadeOut(3000)
                }
            });

            return used

        },

        onItemUpdating: function(grid){
            var new_name = grid.item.name;
            var new_type = grid.item.type;
            var new_default_value = grid.item.default_value;

            $.ajax({
                url: '/is_var_valid',
                type: "POST",
                dataType: 'json',
                async:false,
                data: {'id':grid.item.id,'new_name':new_name, "new_type":new_type, "new_default_value":new_default_value},
                success: function(data){
                    valid = data.boolean;
                    message = data.message;
                    $('.alert_red').text(message).show().fadeOut(3000)
                }
            });
            return valid
        },

        onItemInserting:function(grid){
            var new_name = grid.item.name;
            var new_type = grid.item.type;
            var new_default_value = grid.item.default_value;

            $.ajax({
                url: '/is_var_valid2',
                type: "POST",
                dataType: 'json',
                async:false,
                data: {'new_name':new_name, "new_type":new_type, "new_default_value":new_default_value},
                success: function(data){
                    valid = data.boolean;
                    message = data.message;
                    $('.alert_red').text(message).show().fadeOut(3000)
                }
            });
            return valid
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
                    dataType: "json"
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
                        $('.alert_red').text(data.message).show().fadeOut(3000)
                    }

                });
            }
        }

    });



});