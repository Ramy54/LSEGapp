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
        autoload: true,

        fields: [
            { name: "component", title: "Component", type: "text", align: "center"},
            { name: "variable_text", title: "Variables", type: "text", align: "center", filtering:false},
            { type: "control",
                modeSwitchButton: false,

                headerTemplate: function() {
                    return $("<button>").attr("type", "button").text("Add")
                            .on("click", function () {
                                showDetailsDialog("Add", {});
                            });
                }
            }
        ],

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
            }
        }

    });



});