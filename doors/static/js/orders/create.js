function fill_other_fields(data) {
    console.info(function_name(arguments))

    if(data['error']) {
        location.reload(true)
    }
    else {
        var places = data['places']

        $('#id_place').empty()

        places.forEach(function(place, i) {
            place_pk = place[0]
            place_name = place[1]

            $('#id_place').append(
                '<option value="' + place_pk + '">' + place_name + '</option>'
            )
        })
    }
}
