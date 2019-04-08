$ = django.jQuery
$(function () {
    $('#id_c').on('change',function () {
        console.log($(this).val())
        $.ajax({
            url: '/getKeyword/',
            type: 'POST',
            data: {'c':$(this).val()},
            success:function (e) {
                $("#id_k>option").detach()
                let str = ''
                for (i in e){
                    console.log(i)
                    str +=`<option value="${i}">${e[i]}</option>`
                }
                $('#id_k').append(str)
                console.log(str)
            }
        })
    })
})