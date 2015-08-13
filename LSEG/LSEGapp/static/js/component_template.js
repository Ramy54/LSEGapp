/**
 * Created by ramyah on 12/08/2015.
 */

$(function(){

    $('.formset').formset({
        extraClasses: ['row1']
    });

    $('.table').hide()


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
            { name: "component", title: "Component", type: "text", align: "center"},
            { name: "variable_text", title: "Variables", type: "text", align: "center", filtering:false},
            { type: "control",
                modeSwitchButton: false,

                headerTemplate: function() {
                    return $("<button>").attr("type", "button").attr("class","btn btn-s btn-success").text("Add")
                        .on("click", function () {
                            location.href = 'add_component'
                        });
                }
            }
        ],

        onItemDeleting: function(grid){ //Return if a variable is used by other roles
            $.ajax({
                url: '/is_component_used',
                type: "POST",
                dataType: 'json',
                async:false,
                data: {'component_name':grid.item.component},
                success: function(data){
                    used = data.boolean;
                    message = data.message;
                    $('.alert_red').text(message).show().fadeOut(3000)
                }
            });

            return used

        },

        editItem: function(item){
            location.href = 'edit_component_template/' + item.id

        },


        controller:{
            loadData: function(filter) {
                var component_filter = filter.component;


                var deferred = $.Deferred();

                $.ajax({
                    url: '/get_components',
                    type: "POST",
                    dataType: 'json',
                    data: {"component_filter":component_filter},
                    success: function(data){
                        deferred.resolve(data.components_vars);
                    }
                });

                return deferred.promise();
            },

            insertItem: function(item) {
            },

            updateItem: function(item) {
            },

            deleteItem: function(item) {
                var component_name = item.component;

                $.ajax({
                    type: "POST",
                    url: "/delete_component",
                    dataType: "json",
                    data: {'component_name':component_name},
                    success: function(data){

                    }

                });
            }


        }

    });




});