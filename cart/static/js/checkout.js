$(document).ready(function() {

    $('.paywithRazorPay').click(function(e) {
        e.preventDefault();

        var fname = $("[name='fname']").val()
        var lname = $("[name='lname']").val()
        var email = $("[name='email']").val()
        var phone = $("[name='phone']").val()
        var address = $("[name='address']").val()
        var city = $("[name='city']").val()
        var state = $("[name='state']").val()
        var country = $("[name='country']").val()
        var pincode = $("[name='pincode']").val()
        var new_price = $("[name='new_price']").val()
        var coupon_code2 = $("[name='coupon_code2']").val()
        var token = $("[name='csrfmiddlewaretoken']").val();

        if (fname == "" || lname == "" || email == "" || phone == "" || address == ""|| city == ""|| state == "" || country == ""|| pincode == "")
        {
            
            swal("Alert!", "All fields are mandatory!", "error");
            return false;

        }
        else
        {
            $.ajax({
                method : "GET",
                url : "/proceed-to-pay",
                data : {
                    "new_price" : new_price,
                    "coupon_code2" : coupon_code2,
                    csrfmiddlewaretoken : token
                },
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
                                "fname" : fname,
                                "lname" : lname,
                                "email" : email,
                                "phone" : phone,
                                "address" : address,
                                "city" : city,
                                "state" : state,
                                "country" : country,
                                "pincode" : pincode,
                                "new_price" : new_price,
                                "coupon_code2" : coupon_code2,
                                "payment_mode" : "Paid by Razorpay",
                                "payment_id" : responseb.razorpay_payment_id,
                                 csrfmiddlewaretoken : token
                            }
                            $.ajax({
                                method : "POST",
                                url : "/place-order",
                                data : data,
                               
                                success : function(responseC) {
                                    swal("Congratulations!",responseC.status,"success").then((value) => {
                                        window.location.href = 'my-orders'
                                      });
                                    
                                }
                            })
                            
                        },
                        "prefill": { //We recommend using the prefill parameter to auto-fill customer's contact information, especially their phone number
                            "name": fname + " "+ lname, //your customer's name
                            "email": email, 
                            "contact": phone  //Provide the customer's phone number for better conversion rates 
                        },
                        
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