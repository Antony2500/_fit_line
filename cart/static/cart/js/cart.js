function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');



// Remove item from cart  ( For Cart application )
// Видалити товар з кошика ( Для додатку "Кошик" )
let removeButtons = document.querySelectorAll(".remove-from-cart");

removeButtons.forEach(button => {
  button.addEventListener("click", removeFromCart);
});

function removeFromCart(e) {
  let product_id = e.currentTarget.getAttribute("data-product-id");
  let url = "remove_from_cart";

  let data = {id: product_id};

  fetch(url, {
    method: "POST",
    headers: {"Content-Type": "application/json", 'X-CSRFToken': csrftoken},
    body: JSON.stringify(data)
  })
  .then(res => res.json())
  .then(data => {
    console.log(data);
    location.reload();
  })
  .catch(error => {
    console.log(error);
  });
}


// Change the quantity of goods in the cart ( For Cart application )
// Змінити кількість товару у корзині ( Для додатку "Кошик" )
const changeButtons = document.querySelectorAll(".qt-minus, .qt-plus");

changeButtons.forEach(btn => {
    btn.addEventListener("click", changeQuantity);
});

function changeQuantity(e) {
    const product_id = e.target.getAttribute("data-product-id");
    const change = parseInt(e.target.getAttribute("data-change"));

    const url = "/cart/update_quantity";

    const data = { id: product_id, change: change };

    fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json", "X-CSRFToken": csrftoken },
        body: JSON.stringify(data),
    })
        .then((res) => res.json())
        .then((data) => {
            console.log(data);
            if (data.message === "Quantity updated successfully") {
                // Обновляем отображение количества на странице
                const quantityElement = document.getElementById(`quantity-${product_id}`);
                const newQuantity = parseInt(quantityElement.textContent) + change;
                quantityElement.textContent = newQuantity;


                const productPriceElement = document.getElementById(`price-${product_id}`);
                const initialProductPrice = parseFloat(productPriceElement.getAttribute("data-initial-price")); // Отримуємо початкову ціну товару
                const newPrice = initialProductPrice * newQuantity; // Обчислюємо нову ціну
                productPriceElement.textContent = newPrice.toFixed(2);


                // Обновляем отображение общей суммы на странице
                const totalAmountElement = document.getElementById("totalamount");

                const currentTotalAmount = parseFloat(totalAmountElement.textContent);

                const newTotalAmount = currentTotalAmount + (initialProductPrice * change); // Обчислюємо нову суму
                totalAmountElement.textContent = newTotalAmount.toFixed(2);
            }
        })
        .catch((error) => {
            console.log(error);
        });
}

