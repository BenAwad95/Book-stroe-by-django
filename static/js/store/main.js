function isUserAuthenticated(){
    if(user != 'AnonymousUser'){
        return true
    }else{
        return false
    }
}

function getToken(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
// const csrftoken = getToken('csrftoken')




function getCookie(name) {
    // Split cookie string and get all individual name=value pairs in an array
    var cookieArr = document.cookie.split(";");

    // Loop through the array elements
    for(var i = 0; i < cookieArr.length; i++) {
        var cookiePair = cookieArr[i].split("=");

        /* Removing whitespace at the beginning of the cookie name
        and compare it with the given string */
        if(name == cookiePair[0].trim()) {
            // Decode the cookie value and return
            return decodeURIComponent(cookiePair[1]);
        }
    }


    // Return null if not found
    return null;
}

let cart = JSON.parse(getCookie('cart'))
// console.log('output of getCookie: ',cart)
if(cart == undefined){
    cart = {}
    document.cookie = 'cart=' + JSON.stringify(cart) + ';domain=;path=/'
    // console.log(cart)
}


function updateCart(action,productId){
    // console.log('it is working')
    fetch('/update-cart/',{
        method:'POST',
        headers:{
            'Content-Type': 'application/json',
            'X-CSRFToken': getToken('csrftoken'),
        },
        body:JSON.stringify({
            'productId':productId,
            'action':action,
        })
    })
    .then(res =>{return res.json()})
    .then(data =>{
        // console.log(data)
        location.reload()
    })
}

function addCookieItem(action, productId){
    if(action == 'add'){
        if(cart[productId] == undefined){
            cart[productId] = {'quantity':1}
        }else{
            cart[productId]['quantity'] ++
        }
    }else if(action == 'remove'){
        cart[productId]['quantity'] -= 1
        if(cart[productId]['quantity'] <= 0){
            delete cart[productId]
        }
    }else{
        console.log('There is something wrong here')
    }
    document.cookie = 'cart=' + JSON.stringify(cart) + ';domain=;path=/'
    location.reload()
    // console.log('Updated cart: ',cart)
}