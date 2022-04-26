jQuery(function($) {
    $(document).ready(function() {
        $("#id_brand").change(function() {
            var brand = $(this).val();
            var category = $("#id_category").val();
            var csrftoken = $('[name="csrfmiddlewaretoken"]').val();

            data = {
                    'brand': brand,
                    'category': category,
                    csrfmiddlewaretoken: csrftoken,
                },
                $.ajax({
                    url: 'http://127.0.0.1:8000/core/select_model/',
                    type: 'POST',
                    data: data,
                    dataType: "json",
                    cache: false,
                    success: function(response) {
                        $("#id_model").empty();
                        var myArray = [];
                        myArray = response['data']

                        $.each(myArray, function(i) {
                            var option = $('<option />');
                            option.attr('value', myArray[i].id).text(myArray[i].model);

                            $('#id_model').append(option);
                        });
                    },
                    error: function(jqXHR, textStatus, errorThrown) {
                        if (jqXHR.status == 500) {
                            alert('Internal error: ' + jqXHR.responseText);
                        } else {
                            alert('Unexpected error.');
                        }
                    }
                });
        });
    });
});