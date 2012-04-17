function update_steps(data) {
    console.info(function_name(arguments))

    if(data['error']) {
        location.reload(true)
    }
    else {
        var total_steps    = data['total_steps']
        var disabled_steps = data['disabled_steps']
        var step_pk        = data['step_pk']
        var datetime       = data['datetime']

        var i
        for(i = 1; i <= total_steps; i++) {
            console.log('disabled_steps.indexOf(' + i + ')', disabled_steps.indexOf(i))

            // If it's -1, then it's not in disabled_steps.
            if(disabled_steps.indexOf(i) >= 0) {
                console.log(i + ' needs to be disabled')

                $('#step_' + i).attr('disabled', 'disabled')
            }
            else {
                console.log(i + ' needs to be enabled')

                $('#step_' + i).removeAttr('disabled')
            }

            if(i == step_pk) {
                $('#step_' + i + '_datetime').text(datetime)
            }
        }
    }
}
