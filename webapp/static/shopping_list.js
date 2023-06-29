$(document).on("click", ".rename-shopping-list", function () {
     var shopping_list_id = $(this).data('id');
     console.log(shopping_list_id)
     $("#rename_shopping_list #shopping_list_id").val( shopping_list_id );
    });

