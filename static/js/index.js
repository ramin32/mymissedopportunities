$(document).ready(function() {
    $(".selected").removeAttr("href");

    $('#submit_link').click(function(){
        $('.post_form').slideToggle();
        return false;
    });

    $('.post_form, .comment_form').submit(submit_form);

    $(".vote_link").click(vote);
    $('.comment_link').click(insert_comment_form);
    $('#login_form').find('input[type=text], input[type=password]').focus(function()
    {
        $(this).val('');
        $(this).unbind('focus');
    }); 

    if($.browser.msie) {
        $('#user_meta span').css('borderWidth','1');
    }
});

function insert_comment_form()
{
    $(".post_form, .comment_form").hide();
    $(this).hide();
    $('.comment_link').show();
    var comment_form = $(this).parent().find('.comment_form');
    comment_form.show();
    return false;
}

function vote() {
        var vote_span = $(this).siblings('.votes');
        var old_val = parseInt(vote_span.html());
        $.post($(this).attr('href'), function() {
            vote_span.html(old_val + 1);
        });

        $(this).removeAttr('href')
        .unbind('click')
        .removeClass('active_link vote_link')
        .addClass('inactive_link');
        return false;
}

function submit_form()
{
    var form = $(this);
    var form_data = form.serialize(); 
    $.ajax(
        {
            type: form.attr('method'),
            url: form.attr('action'), 
            data: form_data, 
            success: function(data, status, xhr){
                var json_response = $.parseJSON(data);
                if(json_response.status == "success")
                {
                  form.after(json_response.html);
                  if(form.hasClass('post_form'))
                  { 
                      form.next().find('.vote_link').click(vote);
                      form.next().find('.comment_link').click(insert_comment_form);
                      form.next().find('.comment_form').submit(submit_form);
                  }
                  else if(form.hasClass('comment_form'))
                  {      
                      form.parent().find('.comment_link').show();
                  }
                    reset(form);
                    form.hide();
                 }
                 else {
                    form.find('.dynamic_part').replaceWith(json_response.html);
                 }
            },
            error: function(xhr, status, error){
                 alert("There was a problem with your post.");
            }
        }
    );
    return false;
}

function reset(form)
{
    form.find('textarea, select').val('');
}
