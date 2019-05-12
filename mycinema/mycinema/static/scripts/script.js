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

    if($("#booked-movies-list")) {
        populate_booked_movies()
    }
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

        $('#book-now-modal input[name=row]').val(row)
        $('#book-now-modal input[name=col]').val(col)

        $('#book-now-modal').modal('show')
    })
}

function populate_booked_movies() {
    var loc = $("#booked-movies-list")
    var html = '<div class="list-group-item">Booked movies:</div>';
    $.get("/api/notifications")
    .done(data => {
        var els = data.tickets
        if(els.length == 0){
            html += '<div class="list-group-item"><em>No movies booked...</em></div>'
        }
        
        for(var el of els){
            html += `<a href="/movies/${el.movie_id}" class="list-group-item list-group-item-action">
                <img src="/media/${el.movie_photo}" class="movie_icon_drd">
                <b>${el.movie_name}</b><br>
                <span>${el.show_datetime}</span>
            </a>`
        }
        loc.html(html)
    })
}
