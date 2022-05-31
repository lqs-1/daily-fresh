
function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(function (){
    update_sku_amount()
})

$('#tag_detail').click(function () {
  $('#tag_comment').removeClass('active')
  $(this).addClass('active')
  $('#tab_detail').show()
  $('#tab_comment').hide()
})

$('#tag_comment').click(function () {
  $('#tag_detail').removeClass('active')
  $(this).addClass('active')
  $('#tab_detail').hide()
  $('#tab_comment').show()
})




 // 计算商品的小计
        function update_sku_amount() {
            count = $('.num_show').val();
            price = $('.show_pirze').children('em').text();
            goods_name = $("#goods_name").text()
            // 计算小计
            amount = parseFloat(price) * parseInt(count);
            // 设置商品的小计
            $('.buy_btn').attr('href', 'http://127.0.0.1:8000/order/pay?goods_name='+goods_name+'&goods_count='+count+'&goods_totail='+amount)
            $('.total').children('em').text(amount.toFixed(2)+'元');

        }
       // 商品数量增加
        $('.add').click(function () {
            // 获取商品的数量
            var count = parseInt($('.num_show').val())
            var goods_count = $("#goods_count").text()
            goods_count = goods_count.replace("数 量：", "")
            if (count >= goods_count){
                 $('.num_show').val(goods_count);
            }else {
                count = parseInt(count)+1;
                // 重新设置商品的数量
                $('.num_show').val(count);
            }

            // 重新计算小计
            update_sku_amount()

        });
        // 商品数量减少
       $('.minus').click(function () {
           count = $('.num_show').val();
           count = parseInt(count)-1;
           if (count <= 0) {
               count = 1;
           }
           $('.num_show').val(count);
           update_sku_amount();
       });

    $(".add_cart").click(function () {
        var goods_id = $("#goods_id").text()
        var goods_name = $("#goods_name").text()
        var goods_price = $(".show_pirze").text()
        var goods_unit = $(".show_unit").text()
        var goods_count = $(".num_show").val()


        var context = {
            "goods_id": goods_id,
            "goods_name": goods_name,
            "goods_price": goods_price,
            "goods_unit": goods_unit,
            "goods_count": goods_count,
            "csrfmiddlewaretoken": getCookie("csrftoken"),
        }

        $.post('http://127.0.0.1:8000/cart/add', context, function (response) {
            if (response.errno == '1') {
                alert(response.errmsg)
            }
        })
    })








// $(".buy_btn").click(function () {
//     var goods_id = $("#goods_id").text()
//     var goods_name = $("#goods_name").text()
//     var goods_price = $(".show_pirze").text()
//     var goods_unit = $(".show_unit").text()
//     var goods_count = $(".num_show").val()
//     var goods_totail = $(".total").text()
//     var context = {
//             "goods_id": goods_id,
//             "goods_name": goods_name,
//             "goods_price": goods_price,
//             "goods_unit": goods_unit,
//             "goods_count": goods_count,
//             "goods_totail": goods_totail,
//         }
//      $.post('http://127.0.0.1:8000/order/pay', context, function (response) {
//             if (response.errno == '1') {
//                 window.location.href = 'http://127.0.0.1:8000/order/pay'
//             }
//         })
// })