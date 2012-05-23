function update_steps(data) {
    console.info(function_name(arguments))

    if(data['error']) {
        location.reload(true)
    }
    else {
        var checked        = data['checked']
        var total_steps    = data['total_steps']
        var disabled_steps = data['disabled_steps']
        var step_pk        = data['step_pk']
        var datetime       = data['datetime']
        var user           = data['user']
        var comment_pk     = data['comment_pk']
        var comment        = data['comment']

        console.log('checked', checked)

        var i
        for(i = 1; i <= total_steps; i++) {
            console.log('disabled_steps.indexOf(' + i + ')', disabled_steps.indexOf(i))

            // If it's -1, then it's not in disabled_steps.
            if(disabled_steps.indexOf(i) >= 0) {
                console.log(i + ' needs to be disabled')

                $('#step-' + i).attr('disabled', 'disabled')
            }
            else {
                console.log(i + ' needs to be enabled')

                $('#step-' + i).removeAttr('disabled')
            }

            if(i == step_pk) {
                $('#step-' + i + '-datetime').text(checked ? datetime : 'None')
            }
        }

        $('#no-comments').remove()
        $('#comment-count').text(parseInt($('#comment-count').text()) + 1)

        var full_comment = datetime + ' - ' + comment
        $('#comment-list').append('<div id="comment-' + comment_pk + '" class = "round info-box smaller">' + full_comment + '</div>').scrollTo('100%')
    }
}
