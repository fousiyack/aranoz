$(document).ready(function () {
  $("#payWithRazorpay").click(function (e) {
    e.preventDefault();

    var first_name = $("[name='first_name']").val();
    var last_name = $("[name='last_name']").val();
    var email = $("[name='email']").val();
    var phone = $("[name='phone']").val();
    var address_line_1 = $("[name='address_line_1']").val();
    var address_line_2 = $("[name='address_line_2']").val();
    var city = $("[name='city']").val();
    var state = $("[name='state']").val();
    var country = $("[name='country']").val();
    var zip_code = $("[name='zip_code']").val();
    var token = $("[name='csrfmiddlewaretoken']").val();

    if (
      first_name == "" ||
      last_name == "" ||
      email == "" ||
      phone == "" ||
      address_line_1 == "" ||
      city == "" ||
      state == "" ||
      country == "" ||
      zip_code == ""
    ) {
      swal("alert", "All fields are mandatory", "error");
      return false;
    } else {
      $.ajax({
        method: "GET",
        url: "/orders/proceed-to-pay",
        contentType: "application/json",
        success: function (response) {
          var options = {
            key: "rzp_test_HqkHmr4VjtnaDO", // Enter the Key ID generated from the Dashboard
            amount: response.total_price * 100, //response.total_price *100 , // Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
            currency: "INR",
            name: "Brotoz",
            description: "Thank you",
            image: "https://example.com/your_logo",
            // "order_id": "order_IluGWxBm9U8zJ8", //This is a sample Order ID. Pass the `id` obtained in the response of Step 1
            handler: function (responseb) {
              // alert(responseb.razorpay_payment_id);
              // alert(response.razorpay_order_id);
              // alert(responseb.razorpay_payment_id);
              data = {
                first_name: first_name,
                last_name: last_name,
                email: email,
                phone: phone,
                address_line_1: address_line_1,
                address_line_2: address_line_1,
                city: city,
                state: state,
                country: country,
                zip_code: zip_code,
                payment_mode: "Paid by Razorpay",
                payment_id: responseb.razorpay_payment_id,
                csrfmiddlewaretoken: token,
              };

              $.ajax({
                method: "POST",
                url: "/orders/place_order/",
                data: data,
                success: function (responsec) {
                  swal("Congratulations!", responsec.status, "success").then(
                    (value) => {
                      window.location.href =
                        "/orders/order-complete/" +
                        "?payment_id=" +
                        data.payment_id;
                    }
                  );
                },
              });
            },
            prefill: {
              name: first_name + " " + last_name,
              email: email,
              contact: phone,
            },
            notes: {
              address: "brotoz shopping site",
            },
            theme: {
              color: "#3399cc",
            },
          };
          var rzp1 = new Razorpay(options);
          rzp1.open();
        },
      });
    }
  });
});
