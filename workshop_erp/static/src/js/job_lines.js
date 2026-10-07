/** @odoo-module **/
import publicWidget from "@web/legacy/js/public/public_widget";
publicWidget.registry.JobLineRequest = publicWidget.Widget.extend({
   selector: "#wrap",
   events: {
       'click  .remove_list': '_onClickRemoveList',
       'click .add_total_project': '_onClickAddJobLine',
       'click .remove_line': '_onClickRemoveLine',
       'change .product_id':'_onChangeProduct',
       'change .quantity':'_onChangeQuantity',
       'change .price_unit':'_onChangePrice',
       'change .sub_total':'_onChangeSubTotal',
       // 'change .customer_id':'_onChangeCustomer',
       },

    _onChangePrice:function(ev){
        var $row = $(ev.target).closest('tr');
            let row_quantity = $row.find('input[name="quantity"]').val();
            let row_price = $row.find('input[name="price_unit"]').val();
            var sub_total = row_quantity * row_price
            $row.find('#sub_total').val(sub_total);
             var total = 0
             $('#job_line_table tbody tr.job_order_line').each(function () {
                 var subtotal = $(this).find('#sub_total').val();
                 total += parseFloat(subtotal)
                 console.log("k",subtotal)
                 console.log("o",total)
             });
            $('#total').val(total);
    },

    _onChangeQuantity: function(ev) {
         console.log('ll')
            var $row = $(ev.target).closest('tr');
            let row_quantity = $row.find('input[name="quantity"]').val();
            let row_price = $row.find('input[name="price_unit"]').val();
            var sub_total = row_quantity * row_price
            $row.find('#sub_total').val(sub_total);
            var total = 0
             $('#job_line_table tbody tr.job_order_line').each(function () {
                 var subtotal = $(this).find('#sub_total').val();
                 total += parseFloat(subtotal)
                 console.log("k",subtotal)
                 console.log("o",total)
             });
            $('#total').val(total);
    },

    _onChangeProduct: function(ev) {
            console.log('ll')
            var $row = $(ev.target).closest('.job_order_line');
            var $selected = $(ev.target).find('option:selected')
            var price = parseFloat($selected.attr('data-price'))
            $row.find('#price_unit').val(price);
            $row.find('#quantity').val("1")
            $row.find('#sub_total').val(price);
            var total = 0
             $('#job_line_table tbody tr.job_order_line').each(function () {
                 var subtotal = $(this).find('#sub_total').val();
                 // s= parseFloat(subtotal)
                 total += parseFloat(subtotal)
                 console.log("k",subtotal)
                 console.log("o",total)
             });

            $('#total').val(total);
        },

    _onClickAddJobLine: function(ev) {
       console.log("!!! Odoo OWL Button successfully clicked !!!");
       var $new_row = $('#job_line_table tbody tr.job_order_line:first').clone();
       $new_row.find('input, select').val('');  // Clear input values
       $new_row.appendTo('#job_line_table tbody');
   },

   _onClickRemoveLine: function(ev) {
       console.log('print')
       if ($('#job_line_table tbody tr').length > 1) {
        $(ev.target).closest('tr').remove();
       } else {
           alert("You must have at least one job line.");
       }
   },

    _onClickRemoveList: function(ev) {
       console.log('remove')
       $(ev.target).closest('tr').remove();
       },

    // _onChangeCustomer:function(ev) {
    //    console.log("app")
    //     var customerId = $(ev.target).val();
    //    console.log(customerId)
    //     var $vehicle = $('#vehicle_id');
    //           console.log($vehicle)
    //
    //     $vehicle.find('option').each(function () {
    //         var ownerId = $(this).attr('data-owner')
    //         console.log(ownerId)
    //         if (ownerId == customerId) {
    //             $(this).show()
    //         } else {
    //             $(this).hide()
    //         }
    //     });
    //     // $('#vehicle').val('')
    // },
});
