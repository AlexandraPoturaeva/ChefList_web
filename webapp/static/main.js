$(document).ready(

function () {
/*
JavaScript package "moment.js" helps to display date
in the datatable below in a desired format 'DD.MM.YYYY'.
*/
    $.fn.dataTable.moment( 'DD.MM.YYYY' );

/*
DataTables is a plug-in for the jQuery Javascript library.
The code below converts a Bootstrap 5 table with id "my_shopping_lists" to a datatable with such
options: search, sort, navigate through it's pages, choose how many entries to show.
*/
    $('#my_shopping_lists').DataTable(
        {
            "columnDefs": [
                { "orderable": false, "targets": [1, 3, 4] } // set feature of sorting only for 2, 3, 4 columns
                ],
            "order": [],
            "language": { // translate DataTable labels to Russian language
                "emptyTable": "Таблица пока пустая",
                "info": "Показаны с _START_ по _END_ из _TOTAL_",
                "infoEmpty":  "Показаны с 0 по 0 из 0",
                "infoFiltered":   "(отфильтровано из _MAX_)",
                "lengthMenu": "Показать _MENU_",
                "loadingRecords": "Загрузка...",
                "processing": "",
                "search": "Поиск:",
                "zeroRecords": "Ничего не найдено",
                "paginate": {
                    "next": "Вперёд",
                    "previous": "Назад"
                }
            }
        }
    );

/*
The code below is an event handler to the "click" event
on the element (button) with id "rename_shopping_list_button".
Function creates variable and assigns to it a value of element_id got from the button.
After this function passes this data (element_id) to a form in the modal fade with id "rename_shopping_list_modal".
*/
    $(document).on("click", "#rename_shopping_list_button", function () {
         var element_id = $(this).data('id');
         $("#rename_shopping_list_modal #element_id").val( element_id );
    });

/*
The code below is an event handler to the "click" event
on the element (button) with id "edit_quantity".
Function creates variable and assigns to it a value of element_id got from the button.
After this function passes this data (element_id) to a form in the modal fade with id "edit_quantity_modal".
*/
    $(document).on("click", "#edit_quantity", function () {
         var element_id = $(this).data('id');
         $("#edit_quantity_modal #element_id").val( element_id );
    });

/*
The code below is an event handler to the "change" event
on a input (checkbox) with class ended with "check-item".
*/
    $('input.check-item').change(function() {

        var checked = 0; // assign a variable with default value "false"

        if ($(this).is(':checked')) { // if checkbox is checked

            checked = 1; // change value to "true"

            $(this) // move this element to the end of the list
                .parents('ul.shopping-list')
                .append($(this)
                .parents('li.shopping-list-item'));

            $(this)// add to class of checkbox label 'text-decoration-line-through' (make text line-through)
                .next()
                .addClass('text-decoration-line-through');

        } else { // if checkbox is unchecked

            $(this) // move this element to the top of the list
                .parents('ul.shopping-list')
                .prepend($(this)
                .parents('li.shopping-list-item'));

            $(this) // remove 'text-decoration-line-through' from class of checkbox label
                .next()
                .removeClass('text-decoration-line-through'); // make text common again (not line-through)
        }

        // send data to the server using a HTTP POST request
        $.post(
            "/shopping_lists/shopping-item-checkbox", // url to which the request is sent
            {
                item_id: $(this).data('id'), // data sent to the url (value of data-id of checkbox)
                state_of_checkbox: checked // another data sent to the url (value of the variable "checked")
            },
            function( data ) { // get value returned from url ('ok' of 'failed') and show it in console
                console.log(data);
            }
        );
    });

/*
The code below is an event handler to the "submit" event
in the form containing "add-item-form" in it's class.
Function compares text got from the field with id "new_item_name"
with each label with class containing "item-name".

If these texts are equal to each other, function:
 1. adds 'list-group-item-danger' to the class of 'li.shopping-list-item'
 2. puts a message "Такой продукт уже есть в списке" into a "div.space-for-messages"
 3. prevents submitting of the form
 4. stops iteration
*/

    $(".add-item-form").submit(function(e) {
        var new_item_name = $("#new_item_name").val();

        $('label.item-name').each(function() {
            var item_name = $(this).text().trim();

            if (item_name.toLowerCase() == new_item_name.toLowerCase()) {

                let li = $(this).parents('li.shopping-list-item')
                li.addClass('list-group-item-danger');
                $('.space-for-messages').text('Такой продукт уже есть в списке').css("color", "red")

                setTimeout(function() {
                    li.removeClass('list-group-item-danger');
                    $('.space-for-messages').empty();
                    }, 3000);

                e.preventDefault();
                return false;
            }
        });
    });

/*
The code below is an event handler to the "click" event
on the button containing "add-ingredients-from-recipe" in it's class.

What it is doing:
1. getting data from the button (recipe_id and shopping_list_public_id)
   and value from the input with id "#select_portions_" + recipe_id.
2. selecting elements (button and it's svg path)
3. sending data to the url "/choose_recipe_to_add/" + shopping_list_public_id using a HTTP POST request
4. if it's done - change colour of the button to red and replace it's svg.
If it's failed - puts message 'Что-то пошло не так...' into the padding with '.space-for-messages'
*/

    $(document).on("click", ".add-ingredients-from-recipe", function () {
         var recipe_id = $(this).data('recipe-id');
         var shopping_list_public_id = $(this).data('shopping-list-public-id');
         var portions = $("#select_portions_" + recipe_id).val();

         let add_button = $(this)
         let button_svg_path = $(this).children('svg').children('path.svg-path');

         $.post(
            "/shopping_lists/choose_recipe_to_add/" + shopping_list_public_id,
            {recipe_id: recipe_id, portions: portions})
            .done(function(){
                add_button.removeClass("btn-danger").addClass("btn-success")
                button_svg_path.attr("d", "M2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2zm10.03 4.97a.75.75 0 0 1 .011 1.05l-3.992 4.99a.75.75 0 0 1-1.08.02L4.324 8.384a.75.75 0 1 1 1.06-1.06l2.094 2.093 3.473-4.425a.75.75 0 0 1 1.08-.022z");
            })
            .fail(function(){
                $('.space-for-messages').text('Что-то пошло не так...').css("color", "red");
            });

            setTimeout(function() {
                    $('.space-for-messages').empty();
                    }, 4000);
    });

    $(".add-cooking-step-form").submit(function(e) {
        e.preventDefault();
        var cooking_step_text = $(".new-cooking-step-text").val();
        var recipe_id = $(".add-cooking-step-button").data('recipe-id');

        $.post(
            "/recipes/add_recipe_description/" + recipe_id,
            {cooking_step_text: cooking_step_text}
            )
            .done(function(){
                let step = $('.new-cooking-step-input-group');
                let new_step = step.clone();
                new_step.insertAfter(step);

                step
                .removeClass('new-cooking-step-input-group')
                .find('.new-cooking-step-text')
                .removeClass('new-cooking-step-text')
                .attr("disabled", true);

                new_step.children('.new-cooking-step-text').val('');
                let cnt = parseInt(new_step.children('.cooking-step-num').html());
                new_step.children('.cooking-step-num').html(cnt+1);

            })
            .fail(function(){
                $('.space-for-messages').text('Что-то пошло не так...').css("color", "red");
            });

            setTimeout(function() {
                    $('.space-for-messages').empty();
                    }, 4000);

        });

    $(".add-ingredient-form").submit(function(e) {
        e.preventDefault();
        var product_name = $(".new-ingredient-data").find('.product-name').val();
        var product_category = $(".new-ingredient-data").find('.product-category').val();
        var ingredient_quantity = $(".new-ingredient-data").find('.ingredient-quantity').val();
        var ingredient_unit = $(".new-ingredient-data").find('.ingredient-unit').val();
        var recipe_id = $(".add-ingredient-button").data('recipe-id');

        $.post(
            "/recipes/add_ingredient/" + recipe_id,
            {product_name: product_name,
            product_category: product_category,
            ingredient_quantity: ingredient_quantity,
            ingredient_unit: ingredient_unit}
            )
            .done(function(){

                let ingredient =  $('.new-ingredient-data');

                let new_ingredient = ingredient.clone();
                new_ingredient.insertAfter(ingredient);

                new_ingredient.find('.product-name').val('');
                new_ingredient.find('.ingredient-quantity').val('1');

                ingredient
                .removeClass('new-ingredient-data')
                .find('input,select')
                .prop({disabled: true});
            })
            .fail(function(){
                $('.space-for-messages').text('Что-то пошло не так...').css("color", "red");
            });

            setTimeout(function() {
                    $('.space-for-messages').empty();
                    }, 4000);

        });

    $(document).on("click", ".copy-recipe", function (event) {
        var recipe_info = $(this).data('recipe-info');
        var recipe_id = $(this).data('recipe-id');
        console.log(recipe_id);
        event.preventDefault();
        $.post(
            "/recipes/copy_to_my_recipes",
            {recipe_info: recipe_info})
            .done(function(data){
            window.location = "/recipes/" + data;
            })
            .fail(function(){
                $('.space-for-messages').text('Что-то пошло не так...').css("color", "red");
            });
    });
});

/*
The function below is called from a template.
It inserts a tooltip with title "Ссылка скопирована" after the button clicked,
copies text got from a template to clipboard.
*/
function copy_link_to_clipboard(text, target) {

    setTimeout(function() { // set duration of showing tooltip
        $('#copied_tip').remove();
    }, 800);

    $(target).append("<div class='tip' id='copied_tip'>Ссылка скопирована</div>"); // insert a tooltip

    text =  document.baseURI + text; // add to the text got from a template document.baseURI

    var input = document.createElement('input'); // assign a variable with value of HTML <input> element
    input.setAttribute('value', text); // set the value (text) of an attribute on the <input> element
    document.body.appendChild(input); // add a <input> element to the end of the list of children
    input.select(); // select all the text in an <input> element

    var result = document.execCommand('copy'); // assign a variable with value of the command to copy to the clipboard

    document.body.removeChild(input) // remove created <input> element

    return result;
}