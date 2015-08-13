/**
 * Created by ramyah on 13/08/2015.
 */


$(function(){
    $("#jsGrid").jsGrid({

        width: "100%",
        pageSize: 15,
        pageButtonCount: 5,
        filtering:true,
        sorting:true,
        inserting:false,
        autoload:true,
        editing: false,


        fields: [
            { name: "role", title: "Role", type: "text", align: "center"},
            { name: "component_text", title: "Components", type: "text", align: "center", filtering:false},
            { type: "control",
                modeSwitchButton: false,

                headerTemplate: function() {
                    return $("<button>").attr("type", "button").attr("class","btn btn-s btn-success").text("Add")
                        .on("click", function () {
                            location.href = 'add_role_template'
                        });
                }
            }
        ],

        onItemDeleting: function(grid){ //Return if a variable is used by other roles
            $.ajax({
                url: '/is_role_used',
                type: "POST",
                dataType: 'json',
                async:false,
                data: {'role_name':grid.item.role},
                success: function(data){
                    used = data.boolean;
                    message = data.message;
                    if(message){
                        $('.alert_red').text(message).show().fadeOut(3000)
                    }

                }
            });
            return used

        },


        editItem: function(item){
            location.href = 'edit_role_template/' + item.id

        },


        controller:{
            loadData: function(filter) {
                var role_filter = filter.role;


                var deferred = $.Deferred();

                $.ajax({
                    url: '/get_roles',
                    type: "POST",
                    dataType: 'json',
                    data: {"role_filter":role_filter},
                    success: function(data){
                        deferred.resolve(data.roles_components);
                    }
                });

                return deferred.promise();
            },

            insertItem: function(item) {
            },

            updateItem: function(item) {
            },

            deleteItem: function(item) {
                var role_name = item.role;

                $.ajax({
                    type: "POST",
                    url: "/delete_role_template",
                    dataType: "json",
                    data: {'role_name':role_name},
                    success: function(data){

                    }

                });
            }


        }

    });

});