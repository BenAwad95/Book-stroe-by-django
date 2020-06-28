const addBtns = document.querySelectorAll('.add-item')
const subBtns = document.querySelectorAll('.sub-item')


addBtns.forEach(btn =>{
    btn.addEventListener('click',(e)=>{
        let action = e.target.getAttribute('action')
        let productId = e.target.getAttribute('productId')
        // console.log(action,productId)
        updateCart(action,productId)
    })
})

subBtns.forEach(btn =>{
    btn.addEventListener('click',(e)=>{
        let action = e.target.getAttribute('action')
        let productId = e.target.getAttribute('productId')
        // console.log(action,productId)
        updateCart(action,productId)
    })
})