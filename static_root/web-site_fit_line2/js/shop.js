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



// Open a pop-up window when you click on the "Buy" button ( For Shop application )
// Відкрийте спливаюче вікно при натисканні на кнопку "Купити" ( Для додатку "Магазин" )
document.querySelectorAll('.product-buy').forEach(function(button) {
  button.addEventListener('click', function() {
    document.getElementById('popup').style.display = 'block';
  });
});

document.getElementById('close-popup').addEventListener('click', function() {
  document.getElementById('popup').style.display = 'none';
});


// Filter shop ( For Shop application )
// Фільтр магазину (для додатку "Магазин" )
const burgerMenuButton = document.getElementById("burger-menu-button");
const formShop = document.getElementById("form_shop");
const closeFormButton = document.getElementById("close-form");

if (burgerMenuButton && formShop && closeFormButton) {
  burgerMenuButton.addEventListener("click", () => {
    formShop.style.display = "block";
    closeFormButton.style.display = "block";
  });

  closeFormButton.addEventListener("click", () => {
    formShop.style.display = "none";
    closeFormButton.style.display = "none";
  });
}


// Add to cart func ( For Shop application )
// Функція додавання в кошик ( Для додатку Shop )
let btns = document.querySelectorAll(".productContainer button")

btns.forEach(btn => {
  btn.addEventListener("click", addToCart)
})

function addToCart(e){
    let product_id = e.target.value
    let url = "add_to_cart"

    let data = {id:product_id}

    fetch(url, {
        method: "POST",
        headers: {"Content-Type":"application/json", 'X-CSRFToken': csrftoken},
        body: JSON.stringify(data)
    })
    .then(res=>res.json())
    .then(data=>{
        console.log(data)
    })
    .catch(error=>{
        console.log(error)
    })
}

//
//// Remove item from cart  ( For Cart application )
//// Видалити товар з кошика ( Для додатку "Кошик" )
//let removeButtons = document.querySelectorAll(".remove-from-cart");
//
//removeButtons.forEach(button => {
//  button.addEventListener("click", removeFromCart);
//});
//
//function removeFromCart(e) {
//  let product_id = e.currentTarget.getAttribute("data-product-id");
//  let url = "remove_from_cart";
//
//  let data = {id: product_id};
//
//  fetch(url, {
//    method: "POST",
//    headers: {"Content-Type": "application/json", 'X-CSRFToken': csrftoken},
//    body: JSON.stringify(data)
//  })
//  .then(res => res.json())
//  .then(data => {
//    console.log(data);
//    location.reload();
//  })
//  .catch(error => {
//    console.log(error);
//  });
//}
//
//
//// Change the quantity of goods in the cart ( For Cart application )
//// Змінити кількість товару у корзині ( Для додатку "Кошик" )
//const changeButtons = document.querySelectorAll(".qt-minus, .qt-plus");
//
//changeButtons.forEach(btn => {
//    btn.addEventListener("click", changeQuantity);
//});
//
//function changeQuantity(e) {
//    const product_id = e.target.getAttribute("data-product-id");
//    const change = parseInt(e.target.getAttribute("data-change"));
//
//    const url = "/cart/update_quantity";
//
//    const data = { id: product_id, change: change };
//
//    fetch(url, {
//        method: "POST",
//        headers: { "Content-Type": "application/json", "X-CSRFToken": csrftoken },
//        body: JSON.stringify(data),
//    })
//        .then((res) => res.json())
//        .then((data) => {
//            console.log(data);
//            if (data.message === "Quantity updated successfully") {
//                // Обновляем отображение количества на странице
//                const quantityElement = document.getElementById(`quantity-${product_id}`);
//                const newQuantity = parseInt(quantityElement.textContent) + change;
//                quantityElement.textContent = newQuantity;
//
//
//                const productPriceElement = document.getElementById(`price-${product_id}`);
//                const initialProductPrice = parseFloat(productPriceElement.getAttribute("data-initial-price")); // Отримуємо початкову ціну товару
//                const newPrice = initialProductPrice * newQuantity; // Обчислюємо нову ціну
//                productPriceElement.textContent = newPrice.toFixed(2);
//
//
//                // Обновляем отображение общей суммы на странице
//                const totalAmountElement = document.getElementById("totalamount");
//
//                const currentTotalAmount = parseFloat(totalAmountElement.textContent);
//
//                const newTotalAmount = currentTotalAmount + (initialProductPrice * change); // Обчислюємо нову суму
//                totalAmountElement.textContent = newTotalAmount.toFixed(2);
//            }
//        })
//        .catch((error) => {
//            console.log(error);
//        });
//}


//// cart.js
//// Находим кнопку "Checkout" и всплывающее окно
//const checkoutButton = document.querySelector("#checkout_button");
//
//// Находим всплывающее окно по его id
//const orderPopup = document.getElementById("order-popup");
//
//// Находим кнопки "Отменить" и "Перейти к оплате" во всплывающем окне
//const cancelButton = document.getElementById("cancel-button");
//const paymentButton = document.getElementById("payment-button");
//
//// Добавляем обработчик события для кнопки "Checkout"
//checkoutButton.addEventListener("click", function (e) {
//   e.preventDefault(); // Предотвращаем переход по ссылке
//   orderPopup.style.display = "block"; // Показываем всплывающее окно
//});
//
//// Добавляем обработчики событий для кнопок во всплывающем окне
//cancelButton.addEventListener("click", function () {
//   orderPopup.style.display = "none"; // Скрываем всплывающее окно при отмене
//});