// handle fav button on tag page
$('#favs').click(function(){
    var tagid;
    tagid = $(this).attr("data-tagid");
    $.get('/fav_tag/', {tag_id: tagid}, function(data){
               $('#fav_count').html(data);
               $('#favs').hide();
    });
});

// handle suggestions in side panel
$('#suggestion').keyup(function(){
        var query;
        query = $(this).val();
        $.get('/suggest_tag/', {suggestion: query}, function(data){
         $('#tags').html(data);
        });
});

// handle combobox in add_quote_custom
$(".dropdown-menu li a").click(function(){
        var selText = $(this).text();
        $(this).parents('.input-group').find('.input-select').val(selText);
});