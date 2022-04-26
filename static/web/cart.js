function updateQuantity(productId, b) {

    quantity = $("#quantityId" + productId).val()
    qty = ''
    if (quantity == 0 || quantity == null) {

    } else {
        qty = quantity
        $("#quantityId" + productId).val(qty)
        var sessionid = $("#sessionId").val();


        var csrftoken = $('[name="csrfmiddlewaretoken"]').val();
        data = {
            'session':sessionid,
            'product_id': productId,
            'quantity': qty,
            csrfmiddlewaretoken: csrftoken
        }
        $.ajax({
            url: 'http://127.0.0.1:8000/core/update_cart/',
            type: 'POST',
            data: data,
            success: function(response) {
                updateTotal = response['quantity'] * response['price']
                $("#subTotalPrice" + productId).html('SAR.' + updateTotal + '.0')
                $("#subTotalH6Id").html('SAR.' + response['sub_total'] + '.0')
            }
        });
    }

}

function deleteProduct(productId, df) {

    var csrftoken = $('[name="csrfmiddlewaretoken"]').val();
    var sessionid = $("#sessionId").val();
    data = {
        'session':sessionid,
        'product_id': productId,
        csrfmiddlewaretoken: csrftoken
    }
    $.ajax({
        url: 'http://127.0.0.1:8000/core/delete_cart/',
        type: 'POST',
        data: data,
        success: function(response) {
            $("#cartDataCountVal").html(response['length'])
            var subTotal = $("#subTotalInputId").val();
            finalSubTotal = parseInt(subTotal) - parseInt(response['price'])
            $("#subTotalH6Id").html('SAR.' + finalSubTotal + '.0')
            $(df).closest("li").remove();
            if (response['length'] == '0') {
                $("#subTotalH6Id").html('SAR.' + '0' + '.0')
            }
        }
    });
};



