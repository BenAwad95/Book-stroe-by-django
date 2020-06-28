const formCheckout = document.getElementById("payment-form")

const userInfo = document.getElementById("user-info")

const shippingInfo = document.getElementById('shipping-info')

const paymentWindow = document.getElementById("payment-window")

const payBtn = document.getElementById("pay-btn")

let shippingDetail = {
    'country': null,
    'city': null,
    'street': null,
    'zipCode': null,

}

let order = {}
// console.log(user)

if(user != 'AnonymousUser'){
    userInfo.classList.add('hidden')
}

formCheckout.addEventListener("submit",(e)=>{
    e.preventDefault()
    console.log("You are order complete")
    paymentWindow.classList.remove("hidden")
    shippingDetail.country=formCheckout.country.value
    shippingDetail.city=formCheckout.city.value
    shippingDetail.street=formCheckout.street.value
    shippingDetail.zipCode=formCheckout.zipCode.value
    order = formCheckout.getAttribute('order')
})

payBtn.addEventListener('click',(e)=>{
    e.preventDefault()
    // console.log('payment complete')
    console.log(shippingDetail)
    fetch('/process-order/',{
        method:'POST',
        headers:{
            'Content-Type': 'application/json',
            'X-CSRFToken': getToken('csrftoken'),
        },
        body:JSON.stringify({
            'shippingDetail':shippingDetail,
            'order':order
        })
    })
    .then(res =>{return res.json()})
    .then(data => {
        alert(data)
        goHome()
    })
})


