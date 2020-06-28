const addItemBtns = document.querySelectorAll('.addToCart')


addItemBtns.forEach(btn =>{
    btn.addEventListener('click',(e)=>{
        let action = e.target.getAttribute('action')
        let productId = e.target.getAttribute('productId')
        updateCart(action,productId)
    })
})