
// var options = {
//     "key": "rzp_test_LXZDJ9u8i9F7vG", // Enter the Key ID generated from the Dashboard
//     "amount": 100, // Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
//     "currency": "INR",
//     "name": "ShoeStore",
//     "description": "Purchases",
//     "image": "{% static 'img/vk-high.png' %}",
//     "order_id": "{{payment.id}}", //This is a sample Order ID. Pass the `id` obtained in the response of Step 1
//     "handler": function (response){
//         var  addres = get_address()
//         if (!addres){
//             alert('should select address')
//             return;
//         }
//         window.location.href = `${window.location.origin}/ad/order/ordersuccess/?razorpay_payment_id=${response.razorpay_payment_id}&razorpay_order_id=${response.razorpay_order_id}&razorpay_signature=${response.razorpay_signature}&address=${addres}`
//     },
//     "theme": {
//         "color": "#c20c0c"
//     }
// };
// var rzp1 = new Razorpay(options);
// rzp1.on('payment.failed', function (response){
//         // alert(response.error.code);
//         // alert(response.error.description);
//         // alert(response.error.source);
//         // alert(response.error.step);
//         // alert(response.error.reason);
//         // alert(response.error.metadata.order_id);
//         // alert(response.error.metadata.payment_id);
// });
// document.getElementById('place-order-btn').onclick = function(e){
//     e.preventDefault();
//     console.log('opened');
//     var  addres = get_address()
//     if (!addres){
//         alert('Please select an delivery address')
//         return;
//     }
//     rzp1.open();
// }

// function get_address(){
//     try{
//         var address = document.querySelector('input[name="address"]:checked').getAttribute('id')
//         return address
//     }
//     catch{
//         return;
//     }
// }








// ..............................................................................................

$(document).ready(function() {

    $('.paywithRazorPay').click(function(e) {
        e.preventDefault();
        var token = $("[name='csrfmiddlewaretoken']").val()
        var  addres = get_address()
             if (!addres){
            alert('should select address')
            return;

        }
        else
        {
            $.ajax({
                method : "GET",
                url : "/proceed-to-pay",
                success : function(response){
                    console.log(response);
                    var options = {
                        "key": "rzp_test_BVgJq87xOBXMmk", // Enter the Key ID generated from the Dashboard
                        "amount": response.total_price * 100, // Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
                        "currency": "INR",
                        "name": "VIOLET", //your business name
                        "description": "Thank you for choosing us for your shopping needs.",
                        "image": "{% static 'img/logo.png'%}",
                        //"order_id": "order_9A33XWu170gUtm", //This is a sample Order ID. Pass the `id` obtained in the response of Step 1
                        "handler": function (responseb){
                            alert(responseb.razorpay_payment_id);
                            data = {
                              
                                "address": addres,
                                "payment_mode" : "Paid by Razorpay",
                                "payment_id" : responseb.razorpay_payment_id,
                                csrfmiddlewaretoken: token
                            }
                            $.ajax({
                                method : "POST",
                                url : "/place-order",
                                data : data,
                               
                                success : function(responseC) {
                                    swal("Congratulations!",responseC.status,"success").then((value) => {
                                        window.location.href = 'my-orders'
                                        setTimeout(function() {
                                            location.reload();
                                          }, 500);
                                      });
                                    
                                }
                            })
                            
                        },
                        // "prefill": { //We recommend using the prefill parameter to auto-fill customer's contact information, especially their phone number
                        //     "name": fname + " "+ lname, //your customer's name
                        //     "email": email, 
                        //     "contact": phone  //Provide the customer's phone number for better conversion rates 
                        // },
                        
                        "theme": {
                            "color": "#3399cc"
                        }
                    }
                    var rzp1 = new Razorpay(options);
                    
                    rzp1.open();
                }
            });
            
        }

        
    });

});
function get_address(){
    try{
        var address = document.querySelector('input[name="address"]:checked').getAttribute('id')
        return address
    }
    catch{
        return;
    }
}