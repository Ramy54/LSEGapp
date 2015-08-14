/**
 * Created by ramyah on 14/08/2015.
 */


$(function(){
    var id_env = $( "#id_environment option:selected").val();

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
            {
                headerTemplate: function() {
                    return $("<button>").attr("type", "button").attr("class","generate-button")
                        .on("click", function () {
                            alert("test")
                        });
                },

                itemTemplate: function(_, item) {
                    return $("<input>").attr("type", "checkbox")
                        .on("change", function () {
                            $(this).is(":checked") ? selectItem(item) : unselectItem(item);
                        });
                },
                align: "center",
                width: 50,
                sorting:false
            },
            { name: "host", title: "Host", type: "text", align: "center"},
            { name: "role_text", title: "Roles", type: "text", align: "center", filtering:false},
            { type: "control",
                modeSwitchButton: false,
                editButton: false,

                headerTemplate: function() {
                    return $("<button>").attr("type", "button").attr("class","btn btn-s btn-success").text("Add")
                        .on("click", function () {
                            location.href = 'add_host/' + id_env
                        });
                }
            }
        ],

        onItemDeleting: function(grid){ //Return if a variable is used by other roles


        },


        editItem: function(item){

        },


        controller:{
            loadData: function(filter) {
                var host_filter = filter.host;
                var deferred = $.Deferred();

                $.ajax({
                    url: '/get_hosts',
                    type: "POST",
                    dataType: 'json',
                    data: {"host_filter":host_filter, "id_env":id_env},
                    success: function(data){
                        deferred.resolve(data.host_roles);
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