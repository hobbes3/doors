function fill_other_fields(data) {
    console.info(function_name(arguments))

    if(data['error']) {
        location.reload(true)
    }
    else {
        var properties = data['properties']

        $('#id_property').empty()

        properties.forEach(function(properties, i) {
            property_pk = properties[0]
            property_name = properties[1]

            $('#id_property').append(
                '<option value="' + property_pk + '">' + property_name + '</option>'
            )
        })
    }
}
