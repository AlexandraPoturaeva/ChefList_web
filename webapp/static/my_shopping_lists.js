$(document).ready(function () {
    $.fn.dataTable.moment( 'DD.MM.YYYY' );

    $('#my_shopping_lists').DataTable(
        {
            "columnDefs": [
                { "orderable": false, "targets": 2 }
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

})

