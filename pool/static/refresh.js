
const home = document.querySelector('#home').getAttribute('data-url');

setTimeout(function() {
    location.href = home;
}, 5000);