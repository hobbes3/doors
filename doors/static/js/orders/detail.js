function update_steps(data) {
    console.info(arguments.callee.toString().match(/function\s+([^\s\(]+)/)[1])

    if(data['error']) {
        location.reload(true);
    }
    else {
        var total_steps    = data['total_steps']
        var disabled_steps = data['disabled_steps']
        var step_pk        = data['step_pk']
        var datetime       = data['datetime']

        console.info('disabled_steps', disabled_steps)

        var i
        for(i = 1; i <= total_steps; i++) {
            console.info('disabled_steps.indexOf(' + i + ')', disabled_steps.indexOf(i))

            // If it's -1, then it's not in disabled_steps.
            if(disabled_steps.indexOf(i) >= 0) {
                console.info(i + ' needs to be disabled')

                $('#step_' + i).attr('disabled', 'disabled')
            }
            else {
                console.info(i + ' needs to be enabled')

                $('#step_' + i).removeAttr('disabled')
            }

            if(i == step_pk) {
                $('#step_' + i + '_datetime').text(datetime)
            }
        }
    }
}
