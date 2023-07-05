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
                { "orderable": false, "targets": [2, 3, 4] } // set feature of sorting only for 2, 3, 4 columns
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
on the element (button) with id "rename_button".
Function creates variable and assigns to it a value of element_id got from the button.
After this function passes this data (element_id) to a form in the modal fade with id "rename_modal".
*/
    $(document).on("click", "#rename_button", function () {
         var element_id = $(this).data('id');
         $("#rename_modal #element_id").val( element_id );
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
            "/shopping-item-checkbox", // url to which the request is sent
            {
                item_id: $(this).data('id'), // data sent to the url (value of data-id of checkbox)
                state_of_checkbox: checked // another data sent to the url (value of the variable "checked")
            },
            function( data ) { // get value returned from url ('ok' of 'failed') and show it in console
                console.log(data);
            }
        );
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
