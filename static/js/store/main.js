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



function updateCart(action,productId){
    console.log('it is working')
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
        console.log(data)
        location.reload()
    })
}