/** @odoo-module **/
import publicWidget from "@web/legacy/js/public/public_widget";
publicWidget.registry.MaterialRequest = publicWidget.Widget.extend({
   selector: "#wrap",
   events: {
       'click  .remove_list': '_onClickRemoveLines',
       'click .add_total_project': '_onClickAddMaterial',
       'click .remove_line': '_onClickRemoveLine',
       'change .s_website_form_input':'_onChangeProduct',
       'change .quantity':'_onChangeQuantity',
       'change .price_unit':'_onChangePrice',
       'change .sub_total':'_onChangeSubTotal',
       },

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
            $('#total').val(all_total);



    },

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
                 all_total += parseFloat(subtotal)
                 console.log("k",subtotal)
                 console.log("o",all_total)
             });
            $('#total').val(all_total);
    },

    _onChangeProduct: function(ev) {
            console.log('ll')
            var $row = $(ev.target).closest('.job_order_line');
            var $selected = $(ev.target).find('option:selected')
            var price = parseFloat($selected.attr('data-price'))
            $row.find('#price_unit').val(price);
            $row.find('#quantity').val("1")
            $row.find('#sub_total').val(price);
            var all_total = 0
             $('#material_table tbody tr.job_order_line').each(function () {
                 var subtotal = $(this).find('#sub_total').val();
                 // s= parseFloat(subtotal)
                 all_total += parseFloat(subtotal)
                 console.log("k",subtotal)
                 console.log("o",all_total)
             });

            $('#total').val(parseFloat(all_total));
        },

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

    _onClickRemoveLines: function(ev) {
       console.log('remove')
       $(ev.target).closest('tr').remove();
       // console.log($row)

       // var $row = $(ev.target).closest('tr');
       // $row.remove();
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
