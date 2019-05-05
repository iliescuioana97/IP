$(document).ready(function(){
    setInitialTriggers();
    setBookingHandlers();

    $(".programs .buttons-top button").click(function (e) {
       e.preventDefault();
       $(this).removeClass('active');
    });

})

var setInitialTriggers = function() {
    $(".toggle-menu").on('click', function(e){
        e.preventDefault();
        $(".layout .l-left").toggleClass("on")
    })
    $(".editProfileImage").on('click', function(e){
        e.preventDefault();
        $(".profile_image_upload_hidden").click()
    })

    $(".profile_image_upload_hidden").on('change', function() {
        setProfImgSettings(this)
    });
    $(".settingsContainer .field label").on('click', function(){
        $(this).parent().find("input").focus();
    })
}

function getFocus() {
    document.getElementById("input_search").focus();
}

function setProfImgSettings(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function(e) {
            $('.settingsContainer .image-part .profile').attr('src', e.target.result);
        }

        reader.readAsDataURL(input.files[0]);
    }
}

function setBookingHandlers() {
    $(".room-view-table .chair").on('click', function(e){
        e.preventDefault();

        if($(this).hasClass('booked')) {
            $("#booked-already-modal").modal("show");
            return;
        }

        var row = $(this).data('row');
        var col = $(this).data('col');

        $('#book-now-modal input[name=seat_row]').val(row)
        $('#book-now-modal input[name=seat_col]').val(col)

        $('#book-now-modal').modal('show')
    })
}
