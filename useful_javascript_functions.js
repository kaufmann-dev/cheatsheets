// randomIntFromInterval(min, max);
function randomIntFromInterval(min, max) {
    return Math.floor(Math.random() * (max - min + 1) + min);
}

// .hasScrollbar();
jQuery.fn.hasScrollBar = function () {
    return this.get(0).scrollHeight > this.height();
};

// .clickToggle(function() { ... }, function() { ... });
jQuery.fn.clickToggle = function(a, b) {
    return this.on("click", function(ev) { [b, a][this.$_io ^= 1].call(this, ev) });
};

// .search(elementSelector);
jQuery.fn.search = function(elementSelector) {
    let x = this;
    elementSelector.each(function() {
        if($(this).text().toLowerCase().indexOf(x.val().toLowerCase()) >= 0){
            $(this).css("display", "block");
        } else {
            $(this).css("display", "none");
        }
    });
};
