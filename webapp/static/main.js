$(document).ready(
function () {
    $.fn.dataTable.moment( 'DD.MM.YYYY' );

    $('#my_shopping_lists').DataTable(
        {
            "columnDefs": [
                { "orderable": false, "targets": [2, 3, 4] }
                ],
            "order": [],
            "language": {
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

    $(document).on("click", ".rename", function () {
         var element_id = $(this).data('id');
         $("#rename_modal #element_id").val( element_id );
    });

    $('input.check_item').change(function() {

        var checked = 0;

        if ($(this).is(':checked')) {

            checked = 1;
            $(this).parents('ul.shopping-list').append($(this).parents('li.shopping-list-item'));
            $(this).next().addClass('text-decoration-line-through');

        } else {

            $(this).parents('ul.shopping-list').prepend($(this).parents('li.shopping-list-item'));
            $(this).next().removeClass('text-decoration-line-through');
        }

        $.post(
            "/shopping-item-checkbox",
            {
                item_id: $(this).data('id'),
                state_of_checkbox: checked
            },
            function( data ) {
                console.log(data);
            }
        );
    });
});

function copy(text, target) {
    setTimeout(function() {
        $('#copied_tip').remove();
    }, 800);

    $(target).append("<div class='tip' id='copied_tip'>Ссылка скопирована</div>");
    text =  document.baseURI + text;

    var input = document.createElement('input');

    input.setAttribute('value', text);

    document.body.appendChild(input);
    input.select();

    var result = document.execCommand('copy');

    document.body.removeChild(input)

    return result;
}
