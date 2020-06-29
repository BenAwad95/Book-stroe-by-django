const addBtns = document.querySelectorAll('.add-item')
const subBtns = document.querySelectorAll('.sub-item')


addBtns.forEach(btn =>{
    btn.addEventListener('click',(e)=>{
        let action = e.target.getAttribute('action')
        let productId = e.target.getAttribute('productId')
        // console.log(action,productId)
        if(isUserAuthenticated()){
            updateCart(action,productId)
        }else{
            // console.log("You are not logged in!!")
            addCookieItem(action,productId)
        }
    })
})

subBtns.forEach(btn =>{
    btn.addEventListener('click',(e)=>{
        let action = e.target.getAttribute('action')
        let productId = e.target.getAttribute('productId')
        // console.log(action,productId)
        if(isUserAuthenticated()){
            updateCart(action,productId)
        }else{
            // console.log("You are not logged in!!")
            addCookieItem(action,productId)

        }
    })
})