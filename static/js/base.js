const userPanel = document.getElementById('user-panel')
const userControl = document.getElementById('user-control-container')
userPanel.addEventListener('click',()=>{
    if(userControl.classList.toggle('hidden')){
        userControl.style.display = 'none'
    }else{
        userControl.style.display = 'flex'
    }
})

