function get_data(id)
{
    $.getJSON("/graph", {'id' : id},
        function(data){
            var container = $('#graph')[0];
            if ($.isEmptyObject(data)) {
                container.text('Нет информации в базе данных!');
            } else {
                var network = new vis.Network(container, {}, {} );
                network.setData(data);
            }
        }
    );
}

function update_event()
{
    $('ul li').click(
        function() {
            get_data($(this).attr('id'));

            $('ul li').css("background-color", "");
            $(this).css("background-color", "red");
    });
}


$(document).ready(function() {
    update_event(); //set handler for clicking on the elements of history

    var elements = $('ul li');
    if(elements.length > 0)
    {
        elements[0].click(); //choose the top of the list
    }

    var input = $('input')[0];
    input.style.visibility = "hidden";
    //input.css() not works..

    var preview = $('.preview')[0];

    input.addEventListener('change', function() {
        var curFiles = input.files;

        if(curFiles.length === 0) {
            preview.children[0].textContent = 'Файл не выбран';
            return;
        }

        var file = curFiles[0];

        if (file.size > 1024*1024) {
            preview.children[0].textContent = 'Размер файла <' + file.name + '> превышает 1 МБ';
            return;
        }

        preview.children[0].textContent = 'Загружаем файла <' + file.name + '> ...';

        var formData = new FormData();
        formData.append("file", file);

        var request = new XMLHttpRequest();
        request.open("POST", "/upload", true);
        request.send(formData);
        request.onreadystatechange = function() {
            if (this.status == 200 && this.readyState == 4) {
                preview.children[0].textContent = 'Файл <' + file.name + '> успешно загружен';
                $("form")[0].reset();

                var request2 = new XMLHttpRequest();
                request2.open("GET", "/id", true);
                request2.send();
                request2.onreadystatechange = function() {
                    if (this.status == 200 && this.readyState == 4) {
                        $('ul').prepend(this.responseText);
                        $('#hist')[0].textContent = 'История загрузки: (загружено ' + $('ul li').length + ')'
                        update_event();
                        $('ul li:first').click();
                    }
                }
            }
            else {
                preview.children[0].textContent = 'Файл <' + file.name + '> не загружен';
            }
        }

    });
});
