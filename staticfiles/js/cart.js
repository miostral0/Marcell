
    let user = "{{ request.user|default:'AnonymousUser' }}";

    const updateBtns = document.querySelectorAll('.updateCart');

    updateBtns.forEach(button => {
        button.addEventListener('click', function () {
            const productId = this.dataset.product;
            const action = this.dataset.action;

            if (user === 'AnonymousUser') {
                alert('Please log in to add items to your cart.');
                window.location.href = '/login/';
            } else {
                updateUserOrder(productId, action);
            }
        });
    });

    function updateUserOrder(productId, action) {
        fetch('/update_item/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                'productId': productId,
                'action': action
            })
        })
        .then(response => response.json())
        .then(data => {
            alert(`✅ ${data.message}`);
            // Optional: Update cart count
            if (data.cart_items !== undefined) {
                document.getElementById('cart-count').innerText = data.cart_items;
            }
        });
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    const quantity = document.getElementById('quantity-input').value;

    body: JSON.stringify({
        'productId': productId,
        'action': 'add',
        'quantity': quantity
    })
