var VPR = VPR || {};

VPR.init = function() {
    $('ul.pagination li').click(function() {
        $('ul.pagination li.active').removeClass('active');
        $(this).addClass('active');
        var cardNumber = $.trim($(this).text());
        $('div.group.active_page').removeClass('active_page');
        $('div.page' + cardNumber).addClass('active_page');
    });
};

$(document).ready(function () {
    VPR.init();
});
