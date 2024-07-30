document.addEventListener("DOMContentLoaded", function () {
  addEventListeners();
});

function addEventListeners() {
  const addToCartButtons = document.querySelectorAll(".add-to-cart");
  addToCartButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const coffeeId = this.getAttribute("data-coffee-id");
      addToCart(coffeeId);
    });
  });

  // Use event delegation for delete buttons
  document.body.addEventListener("click", function (event) {
    if (event.target.classList.contains("delete-item")) {
      const itemId = event.target.getAttribute("data-item-id");
      removeFromCart(itemId);
    }
  });
}

function addToCart(coffeeId) {
  fetch("/add_to_cart/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: JSON.stringify({
      coffee_id: coffeeId,
      quantity: 1,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        alert("Coffee added to cart!");
        updateCartSummary(data.cart_total_items, data.cart_total_price);
      } else {
        alert("Error adding coffee to cart. Please try again.");
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("Error adding coffee to cart. Please try again.");
    });
}

function removeFromCart(itemId) {
  fetch(`/remove_from_cart/${itemId}/`, {
    method: "POST",
    headers: {
      "X-CSRFToken": getCookie("csrftoken"),
    },
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        // Remove the item from the DOM
        const cartItem = document.getElementById(`cart-item-${itemId}`);
        if (cartItem) {
          cartItem.remove();
        }

        // Update the cart summary
        updateCartSummary(data.cart_total_items, data.cart_total_price);

        // Update the cart total on the page
        const cartTotal = document.getElementById("cart-total");
        if (cartTotal) {
          cartTotal.innerHTML = `<h3>Total: $${data.cart_total_price.toFixed(
            2
          )}</h3>`;
        }

        // If the cart is empty, show a message
        if (data.cart_total_items === 0) {
          const cartItems = document.getElementById("cart-items");
          cartItems.innerHTML = "<p>Your cart is empty.</p>";
          const checkoutForm = document.querySelector(
            'form[action="/checkout/"]'
          );
          if (checkoutForm) {
            checkoutForm.remove();
          }
        }
      } else {
        alert("Error removing item from cart. Please try again.");
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("Error removing item from cart. Please try again.");
    });
}

function updateCartSummary(totalItems, totalPrice) {
  const cartSummary = document.getElementById("cart-summary");
  if (cartSummary) {
    cartSummary.innerHTML = `<a href="/cart/">Cart: ${totalItems} item(s) - $${totalPrice.toFixed(
      2
    )}</a>`;
  }
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
