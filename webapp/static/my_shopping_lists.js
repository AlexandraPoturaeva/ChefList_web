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

$(document).on("click", ".rename-shopping-list", function () {
     var shopping_list_id = $(this).data('id');
     $("#rename_shopping_list #shopping_list_id").val( shopping_list_id );
    });
