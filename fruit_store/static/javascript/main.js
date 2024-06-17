// Navbar Right section buttons animation 
document.addEventListener("DOMContentLoaded", function () {
    const navbarTogglerBtn = document.getElementById("navbar-toggler-btn");

    // variables for search button animation
    const searchBtn = document.getElementById("search-btn");
    const searchForm = document.querySelector(".search-form");
    const searchInput = document.getElementById("search-box");

    // variables for cart-button animation
    const cartBtn = document.getElementById("cart-btn");
    const cartBox = document.querySelector(".cart-box");


    // variables for profile-button animation
    const profileBtn = document.getElementById("profile-btn");
    const subMenuWrap = document.querySelector(".sub-menu-wrap");

    // Function to handle mouse hover event of search button
    searchBtn.addEventListener("mouseenter", function () {
        searchForm.style.width = "25rem";
        searchForm.style.transition = "0.5s";
        if (cartBox.style.scale > '0' || subMenuWrap.style.maxHeight > '0') {
            cartBox.style.scale = '0';
            subMenuWrap.style.maxHeight = '0rem';

            searchForm.style.width = "25rem";
            searchForm.style.transition = "0.5s";
        } else {
            searchForm.style.width = "25rem";
        }
    });

    // Function to handle mouse hover event of cart button
    cartBtn.addEventListener("mouseenter", function () {
        if (subMenuWrap.style.maxHeight > '1rem' || searchForm.style.width > '0rem') {
            subMenuWrap.style.maxHeight = '0rem';
            searchForm.style.width = '0'

            cartBox.style.scale = "1";
            cartBox.style.transition = "0.5s";
        } else {
            cartBox.style.scale = '1';
            cartBox.style.transition = "0.5s";
        }
    });

    // Function to handle mouse hover event of profile button
    profileBtn.addEventListener("mouseenter", function () {
        if (cartBox.style.scale > '0' || searchForm.style.width > '0') {
            cartBox.style.scale = '0'
            searchForm.style.width = '0'

            subMenuWrap.style.maxHeight = '50rem';
            subMenuWrap.style.transition = "0.5s";
        } else {
            subMenuWrap.style.maxHeight = '50rem';
        }
    });

    // Function to handle search button click event
    searchBtn.addEventListener("click", function () {

        if (searchForm.style.width === "0rem") {
            searchForm.style.width = "25rem";
        } else {
            searchForm.style.width = "0rem";
            searchInput.value = ""; // Clear input when closing search form
        }
    });

    // Function to handle Profile button click event
    profileBtn.addEventListener("click", function () {
        if (subMenuWrap.style.maxHeight === "0rem" || cartBox.style.scale === '1') {
            cartBox.style.scale = '0'
            subMenuWrap.style.maxHeight = "40rem";
        } else {
            subMenuWrap.style.maxHeight = "0rem";
        }

    });

    // function to toggle profile section after closing navbar menu on small screens
    navbarTogglerBtn.addEventListener("click", function () {
        if (subMenuWrap.style.maxHeight > "0rem" || cartBox.style.scale > '0') {
            cartBox.style.scale = '0'
            subMenuWrap.style.maxHeight = "0";
        }
    })


    // Function to handle closing of all menu in buttons after scrolling the screen
    window.addEventListener("scroll", function () {
        if (searchInput.value.trim() === "") {
            searchForm.style.width = "0rem";
        }

        cartBox.style.scale = "0";
        subMenuWrap.style.maxHeight = "0"
    });

});

window.addEventListener("scroll", function () {

    const searchForm = document.querySelector(".search-form");
    const searchInput = document.getElementById("search-box");

    if (searchInput.value.trim() === "") {
        searchForm.style.width = "0rem";
    }
});


// JS for Fixed Nav-bar
let nav = document.querySelector(".navbar");
window.onscroll = function () {
    if (document.documentElement.scrollTop > 20) {
        nav.classList.add("scroll-on");
    } else {
        nav.classList.remove("scroll-on");
    }
}


// Best selling Products Swiper  
var swiper = new Swiper(".mySwiper", {
    slidesPerView: 1,
    spaceBetween: 10,
    loop: true,
    mousewheel: false,
    grabCursor: true,
    pagination: {
        el: ".swiper-pagination",
        clickable: true,
    },
    autoplay: {
        delay: 2500,
        disableOnInteraction: false,
    },
    breakpoints: {
        0: {
            slidesPerView: 1,
            spaceBetween: 20,
        },
        590: {
            slidesPerView: 2,
            spaceBetween: 20,
        },
        767: {
            slidesPerView: 2,
            spaceBetween: 20,
        },
        991: {
            slidesPerView: 3,
            spaceBetween: 20,
        },
        1170: {
            slidesPerView: 4,
            spaceBetween: 20,
        }
    },
    navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
    },
});


// Customer testomonial/ review Section Swiper js
var swiper = new Swiper(".mySwiper2", {
    spaceBetween: 30,
    effect: "fade",
    loop: true,
    grabCursor: true,
    autoplay: {
        delay: 2500,
        disableOnInteraction: true,
    },
    navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
    },
});


// Product Details Page swiper navigation

var swiper = new Swiper(".mySwiper5", {
    pagination: {
        el: ".swiper-pagination",
        type: "fraction",
    },
    navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
    },
});




// ======================================================================================================================================================

$(document).ready(function () {
    $('.add-to-cart-btn').click(function (e) {
        e.preventDefault();

        var productId = $(this).data('product-id');
        var csrftoken = getCookie('csrftoken');

        $.ajax({
            type: 'POST',
            url: '/add_to_cart/' + productId + '/',
            dataType: 'json',
            beforeSend: function (xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            },
            success: function (response) {
                updateCartUI(response);
                displaySuccessMessage(response.message);
            },
            error: function (xhr, status, error) {
                console.error(xhr.responseText);
            }
        });
    });
});


// Function to update the cart UI
function updateCartUI(response) {
    $('.cart-count').text(response.cart_count);
    // You can update other parts of the cart UI here if needed
}

// Function to display success message using SweetAlert
function displaySuccessMessage(message) {
    const Toast = Swal.mixin({
        toast: true,
        position: "top-end",
        showConfirmButton: false,
        timer: 3000,
        timerProgressBar: true,
        didOpen: (toast) => {
            toast.onmouseenter = Swal.stopTimer;
            toast.onmouseleave = Swal.resumeTimer;
        },
        customClass: {
            title: 'popup-title',
            container: 'popup-container',
            popup: 'popup',
        }
    });
    Toast.fire({
        icon: "success",
        title: message,
    });
}

// Function to get CSRF token from cookie
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


// AJAX to remove products from cart dynamically

// Sweetalert for removing products from cart


// Removing all products from cart user permission sweet alert

document.getElementById('clear-cart-button').addEventListener('click', function () {
    Swal.fire({
        title: "Are you sure to Remove all items from cart?",
        text: "You won't be able to revert this!",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Yes, Remove it!"
    }).then((result) => {
        if (result.isConfirmed) {
            fetch("{% url 'clear_cart' %}", {
                method: "POST",
                headers: {
                    "X-CSRFToken": "{{ csrf_token }}"
                }
            }).then(response => {
                if (response.ok) {
                    Swal.fire({
                        title: "Removed!",
                        text: "All Items from cart Removed Successfully.",
                        icon: "success"
                    }).then(() => {
                        window.location.href = "{% url 'index' %}";
                    });
                } else {
                    Swal.fire({
                        title: "Error!",
                        text: "Failed to Remove items From Cart. Please try again later.",
                        icon: "error"
                    });
                }
            })
        }
    });
});
