const addItemBtns = document.querySelectorAll('.addToCart')


addItemBtns.forEach(btn =>{
    btn.addEventListener('click',(e)=>{
        let action, productId;
        if(e.target.classList.contains('btn')){
            action = e.target.getAttribute('action')
            productId = e.target.getAttribute('productId')
        }else{
            action = e.target.parentElement.getAttribute('action')
            productId = e.target.parentElement.getAttribute('productId')
        }
        // console.log(productId,action)        
        if(isUserAuthenticated()){
            updateCart(action,productId)
        }else{
            // console.log("You are not logged in!!")
            addCookieItem(action, productId)
        }
    })
})