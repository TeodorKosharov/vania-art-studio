function alertCompleteOrder(is_cart_empty, total_price) {
    if (is_cart_empty) {
        Swal.fire('Кошницата е празна!');
    } else {
        Swal.fire({
            title: 'Завършване на поръчката?',
            text: `Дължима сума: ${total_price.toFixed(2)} лв.`,
            showCancelButton: true,
            cancelButtonText: 'Отказ',
            confirmButtonText: 'Приключване',
        }).then((result) => {
            if (result.isConfirmed) {
                Swal.fire({
                    position: 'center',
                    icon: 'success',
                    title: 'Поръчката е приключена',
                    showConfirmButton: false,
                    timer: 1500
                });
                setTimeout(redirect, 1600);
            }
        });
    }
}

function redirect() {
    window.location.href = '/complete-order/';
}