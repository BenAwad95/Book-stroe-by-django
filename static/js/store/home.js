const addItemBtns = document.querySelectorAll('.addToCart')


addItemBtns.forEach(btn =>{
    btn.addEventListener('click',(e)=>{
        let action = e.target.getAttribute('action')
        let productId = e.target.getAttribute('productId')
        if(isUserAuthenticated()){
            updateCart(action,productId)
        }else{
            // console.log("You are not logged in!!")
            addCookieItem(action, productId)
        }
    })
})