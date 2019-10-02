'use strict';
document.addEventListener('DOMContentLoaded', function() {
    console.log('hello world')
    var elems = document.querySelectorAll('.carousel');
    var instances = M.Carousel.init(elems);
});