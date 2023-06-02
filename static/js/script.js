document.querySelector('.add').addEventListener('click', function(){
    document.querySelector('.amount-number').value++;
});

document.querySelector('.sub').addEventListener('click', function(){
    amount = document.querySelector('.amount-number');
    if(amount.value > 1){
        amount.value--;
    }
});
