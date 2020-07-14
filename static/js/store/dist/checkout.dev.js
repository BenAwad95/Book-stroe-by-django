"use strict";

var formCheckout = document.getElementById("payment-form");
var userInfo = document.getElementById("user-info");
var visitorUserOptions = document.getElementById('visitor-user-options');
var shippingInfo = document.getElementById('shipping-info');
var paymentWindow = document.getElementById("payment-window");
var payBtn = document.getElementById("pay-btn");
var shippingDetail = {
  'country': null,
  'city': null,
  'street': null,
  'zipCode': null
};
var userForm = {
  'name': null,
  'email': null
};
var order = {}; // console.log(user)

if (isUserAuthenticated()) {
  userInfo.classList.add('hidden');
  visitorUserOptions.classList.add('hidden');
}

formCheckout.addEventListener("submit", function (e) {
  e.preventDefault(); // console.log("You are order complete")

  paymentWindow.classList.remove("hidden");
  shippingDetail.country = formCheckout.country.value;
  shippingDetail.city = formCheckout.city.value;
  shippingDetail.street = formCheckout.street.value;
  shippingDetail.zipCode = formCheckout.zipCode.value;

  if (!isUserAuthenticated()) {
    userForm.name = formCheckout.name.value;
    userForm.email = formCheckout.email.value;
  }
});
payBtn.addEventListener('click', function (e) {
  e.preventDefault(); // console.log('payment complete')
  // console.log(shippingDetail)

  fetch('/process-order/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getToken('csrftoken')
    },
    body: JSON.stringify({
      'shippingDetail': shippingDetail,
      'userForm': userForm,
      'order': order
    })
  }).then(function (res) {
    return res.json();
  }).then(function (data) {
    cart = {};
    document.cookie = 'cart=' + JSON.stringify(cart) + ';domain=;path=/';
    alert(data);
    goHome();
  });
});