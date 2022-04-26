
$("#brand").change(function () {

    var brand = $(this).val();
    var category = $("#category").val();

    var csrftoken = $('[name="csrfmiddlewaretoken"]').val();


    data = {
        'brand': brand,
        'category': category,
        csrfmiddlewaretoken: csrftoken
    }

    $.ajax({

        url: 'http://127.0.0.1:8000/core/model/',
        type: 'POST',
        data: data,
        success: function (response) {

            $("#model").empty();

            var dropdown = $("#model")

            dropdown.append('<option selected="true" disabled>Select Model</option>');
            dropdown.prop('selectedIndex', 0);


            var myArray = [];
            myArray = response['data']

            $.each(myArray, function (i) {


                var option = $('<option />');
                option.attr('value', myArray[i].id).text(myArray[i].model);

                $('#model').append(option);
            });


            var myArray = [];
            myArray = response['product']

            var arrayLength = Object.keys(myArray).length

            if (arrayLength > 0) {
                $('#rowImageViewDiv').empty();


                $.each(myArray, function (i) {

                    target = $('#rowImageViewDiv'),
                        html = ''
                    html = '<div class="col-lg-3 col-6">';
                    html += '<div class="product-item product-item-2">';
                    html += '<div id="viewImage" class="product-img">'
                    html += '<a href="#product">'
                    html += '<img  src="' + myArray[i].image + '" alt="" />'
                    '</a>';
                    '</div>';
                    html += '<div class="product-info">'
                    html += '<h6 class="product-title text-left">'
                    html += '<a href="#product">' + myArray[i].name + '</a>'
                    '</h6>';
                    html += '<h5 class="brand-name" id="brandName">' + myArray[i].brand + '</h5>';
                    html += '<h5 class="brand-name">' + myArray[i].model + '</h5>'
                    html += '<h4 class="pro-price">SAR.' + myArray[i].price + '.00</h4>'
                    '<form>'
                    html += '<button type="button" name="selector" class="btnn mt-3 mb-3" " onclick="btnCart(' + myArray[i].id + ',this)">Add to Cart</button>'
                    '</form>'
                    '</div>'

                    '</div>'


                    '</div>';

                    target.append(html)
                });
            } else {
                alert('No data')


            }
        }
    });
})

$("#model").change(function () {

    var model = $(this).val();
    var brand = $("#brand").val();
    var category = $("#category").val();
    var category = $("#category").val();

    var csrftoken = $('[name="csrfmiddlewaretoken"]').val();
    data = {
        'brand': brand,
        'model': model,
        'category': category,
        csrfmiddlewaretoken: csrftoken
    }

    $.ajax({

        url: 'http://127.0.0.1:8000/core/images/',
        type: 'POST',
        data: data,
        success: function (response) {

            var myArray = [];
            myArray = response['data']

            var arrayLength = Object.keys(myArray).length

            if (arrayLength > 0) {
                $('#rowImageViewDiv').empty();


                $.each(myArray, function (i) {

                    target = $('#rowImageViewDiv');
                    html = '';
                    html = '<div class="col-lg-3 col-6">';
                    html += '<div class="product-item product-item-2">';
                    html += '<div id="viewImage" class="product-img">'
                    html += '<a href="#product">'
                    html += '<img  src="' + myArray[i].image + '" alt="" />'
                    '</a>';
                    '</div>';
                    html += '<div class="product-info">'
                    html += '<h6 class="product-title text-left">'
                    html += '<a href="#product">' + myArray[i].name + '</a>'
                    '</h6>';
                    html += '<h5 class="brand-name" id="brandName">' + myArray[i].brand + '</h5>';
                    html += '<h5 class="brand-name">' + myArray[i].model + '</h5>'
                    html += '<h4 class="pro-price">SAR.' + myArray[i].price + '.00</h4>'
                    '<form>'
                    html += '<button type="button" name="selector" class="btnn mt-3 mb-3" " onclick="btnCart(' + myArray[i].id + ',this)">Add to Cart</button>'
                    '</form>'
                    '</div>'

                    '</div>'


                    '</div>';

                    target.append(html)
                });

            } else {

                alert('No data')
            }

        }
    });
});


function btnCart(productId, thisProp) {
    var csrftoken = $('[name="csrfmiddlewaretoken"]').val();
    var sessionid = $("#sessionId").val();

    data = {
        'session':sessionid,
        'product_id': productId,
        csrfmiddlewaretoken: csrftoken
    }

    $.ajax({

        url: 'http://127.0.0.1:8000/core/cart/',
        type: 'POST',
        data: data,
        beforeSend: function () {
            $(thisProp).prop('disabled', true);
        },
        success: function (response) {
            $("#cartDataCountVal").html(response['length'])
            $(thisProp).prop('disabled', false);

            if (response['msg'] == '1') {
                $(thisProp).html('Already Carted')

            } else {

                $(thisProp).html('Carted')
            }

        },
        // error: function (jqXhr, responseText) {
        //     alert(jqXhr.responseText)
        // }


    });
};