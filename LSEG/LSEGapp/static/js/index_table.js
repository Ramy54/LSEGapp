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
                            generateSelectedItems()
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
                generateButton: true,

                headerTemplate: function() {
                    return $("<button>").attr("type", "button").attr("class","btn btn-s btn-success").text("Add")
                        .on("click", function () {
                            location.href = 'add_host/' + id_env
                        });
                }
            }
        ],






        controller:{
            loadData: function(filter) {
                var id_env = $('#id_environment').val();
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
                var host_id = item.id;

                $.ajax({
                    type: "POST",
                    url: "/delete_host",
                    dataType: "json",
                    data: {'host_id':host_id},
                    success: function(data){

                    }

                });
            }


        }

    });


    var selectedItems = [];

    var selectItem = function(item) {
        selectedItems.push(item);
    };

    var unselectItem = function(item) {
        selectedItems = $.grep(selectedItems, function(i) {
            return i !== item;
        });
    };

    var generateSelectedItems = function() {

        if(!selectedItems.length)
            return;

        var $grid = $("#jsGrid");

        var hosts_ids = [];

        for(var o in selectedItems) {
            hosts_ids.push(selectedItems[o].id);
        }

        $.ajax({
            type: "POST",
            url: "/save_files",
            async:false,
            dataType: "json",
            data: {'myarray': JSON.stringify(hosts_ids)},
            success: function(data){

            }

        });
        location.href = "save_zip/" + id_env; // Call this URL after having saved the selected files

    }

});