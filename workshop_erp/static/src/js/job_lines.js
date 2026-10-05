/** @odoo-module **/
import publicWidget from "@web/legacy/js/public/public_widget";
publicWidget.registry.MaterialRequest = publicWidget.Widget.extend({
   selector: "#wrap",
   events: {
       // 'change .operation': '_onChangeType',
       'click .remove_list_line': '_onClickRemove',
       'click .add_total_project': '_onClickAddMaterial',
       'click .remove_line': '_onClickRemoveLine',
       'change .s_website_form_input':'_onChangeProduct',
       'change .quantity':'_onChangeQuantity',
       'change .price_unit':'_onChangePrice',
       'change .sub_total':'_onChangeSubTotal',
       },

//    _onClickSubmit: async function (ev) {
//        ev.preventDefault();
//        var employee_id = $('#customer').val();
//        var date = $('#date').val();
//        var material_order_ids = [];
//        $('#material_table tbody tr.material_order_line').each(function () {
//            let product = $(this).find('select[name="product"]').val();
//            let quantity = $(this).find('input[name="quantity"]').val();
//            let operation = $(this).find('select[name="price_unit"]').val();
//            let source = $(this).find('select[name="sub_total"]').val();
//            material_order_ids.push({
//                'material': product,
//                'quantity': quantity,
//                'operation_id': operation,
//                'source': source || null,
//            });
//        });
//        // Log data before sending
//        console.log({
//            'employee_id': employee_id,
//            'date': date,
//            'material_order_ids': material_order_ids
//        });
//        try {
//             let response = await rpc('/material/submit', {
//                employee_id: employee_id,
//                date: date,
//                material_order_ids: material_order_ids
//            });
//            console.log('Response:', response);
//            alert('Material request submitted successfully!');
//        } catch (error) {
//            console.error('Error:', error);
//            alert('Failed to submit the material request.');
//        }
// },



    _onChangePrice:function(ev){
        var $row = $(ev.target).closest('tr');
            let row_quantity = $row.find('input[name="quantity"]').val();
            let row_price = $row.find('input[name="price_unit"]').val();
            var total = row_quantity * row_price
            $row.find('#sub_total').val(total);
             var all_total = 0
             $('#material_table tbody tr.job_order_line').each(function () {
                 var subtotal = $(this).find('#sub_total').val();
                 // s= parseFloat(subtotal)
                 all_total += parseFloat(subtotal)
                 console.log("k",subtotal)
                 console.log("o",all_total)
             });
             // let p = $(this).find('#total').val(all_total);
             // console.log("0",p)
            $('#total').val(all_total);

             // $('#material_table tbody tr.job_order_line').each(function () {
             //     var total = 0
             //     var subtotal = $(this).find('input[name="sub_total"]').val();
             //     total += subtotal
             //     $(this).find('#total').val(total);
             // });

    },

    // _updatePrice:function() {
    //     $('#material_table tbody tr.job_order_line').each(function () {
    //         var total = 0
    //         var subtotal = $(this).find('#sub_total').val();
    //         total += subtotal
    //         console.log("k", subtotal)
    //         console.log("o", total)
    //         $(this).find('#total').val(total);
    //
    //     });
    // },

     _onChangeQuantity: function(ev) {
         console.log('ll')
             // this._updateTotal()
            var $row = $(ev.target).closest('tr');
            let row_quantity = $row.find('input[name="quantity"]').val();
            let row_price = $row.find('input[name="price_unit"]').val();
            var sub_total = row_quantity * row_price
            $row.find('#sub_total').val(sub_total);
            var all_total = 0
             $('#material_table tbody tr.job_order_line').each(function () {
                 var subtotal = $(this).find('#sub_total').val();
                 // s= parseFloat(subtotal)
                 all_total += parseFloat(subtotal)
                 console.log("k",subtotal)
                 console.log("o",all_total)
             });
             // let p = $(this).find('#total').val(all_total);
             // console.log("0",p)
            $('#total').val(all_total);
                var employee_id = $('#customer').val();

            let p = $(this).find('input[name="total"]').val(all_total);
            console.log("0",p)
    },

    _onChangeProduct: function(ev) {
            console.log('ll')
            var $row = $(ev.target).closest('tr');
            // var productPrice = $row.find('[data-price]').data('price');
            var productPrice = $row.find('[data-price]').data('price');
            $row.find('#price_unit').val(productPrice);
            $row.find('#quantity').val("1")
            $row.find('#sub_total').val(productPrice);
            var all_total = 0
             $('#material_table tbody tr.job_order_line').each(function () {
                 var subtotal = $(this).find('#sub_total').val();
                 // s= parseFloat(subtotal)
                 all_total += parseFloat(subtotal)
                 console.log("k",subtotal)
                 console.log("o",all_total)
             });
             // let p = $(this).find('#total').val(all_total);
             // console.log("0",p)
            $('#total').val(all_total);
            // $('#total').val(productPrice)
        //
        },

    // _updateTotal: function() {
    //     $('#material_table tbody tr.job_order_line').each(function () {
    //         var total = 0
    //         var subtotal = $(this).find('input[name="sub_total"]').val();
    //         total += subtotal
    //         $(this).find('#total').val(total);
    //     })
    // },




        //  let row_quantity = $row.find('input[name="quantity"]').val();
        // let row_price = $row.find('input[name="price_unit"]').val();
        // var total = row_quantity * row_price
        // $row.find('#sub_total').val(total);


        //     var $row = $(ev.target).closest('tr');
   //     if ($row.find('.operation').val() === "purchase order") {
   //         $row.find('.fields').prop('disabled', true);
   //     } else {
   //         $row.find('.fields').prop('disabled', false);
   //     }
   // }
        // var productPrice = $row.find('data-price').data('price')
        // var productPrice = $('[data-price]').data('price');
        // $row.find('#price_unit').val(productPrice);
        // $row.find('.product').data('price');
        // console.log('ll')


       // $row.update('.price_unit').val() == "l")
       // price_unit.update()
    // },

    _onClickAddMaterial: function(ev) {
       console.log("!!! Odoo OWL Button successfully clicked !!!");
       var $new_row = $('#material_table tbody tr.job_order_line:first').clone();
       $new_row.find('input, select').val('');  // Clear input values
       $new_row.appendTo('#material_table tbody');
       // let product = $(this).find('select[name="product"]').val();
       // var price = $(product).'[data-price]'.data('price');

       // this.$('#quantity').val("1")
       // var productPrice = $new_row.product.$('[data-price]').data('price');
       // $('#price_unit').val(productPrice);
       // var subtotal = val(quantity) * val(price_unit)


   },
   _onClickRemoveLine: function(ev) {
       console.log('print')
       if ($('#material_table tbody tr').length > 1) {
        $(ev.target).closest('tr').remove();
       } else {
           alert("You must have at least one material entry.");
       }
   },

    _onClickRemove: function(ev) {
       console.log('print')
         $(ev.target).this('tr').remove();
       },
   // _onChangeType: function (ev) {
   //     var $row = $(ev.target).closest('tr');
   //     if ($row.find('.operation').val() === "purchase order") {
   //         $row.find('.fields').prop('disabled', true);
   //     } else {
   //         $row.find('.fields').prop('disabled', false);
   //     }
   // }
});
