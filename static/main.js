
  //clear error text 
  $("#new-post textarea").click(function() {
   $(".error").text("")
});
 //call like handler
  $('.like-heart').click(function () {
    var postLike = this
    var dataid = $(this).attr("data-id") 
    $.ajax({
      type: "POST", 
      url: '/blog/' + (dataid) + '/like',
      success: function () { 
      location.reload(); 
      },
      error: function(e) {
      $("#my-modal").modal()
      }
    });
  });
  //call delete-comment handler 
    $('.comment-icon').click(function () {
    var postcomment = this
    //get the comment id from the icon id
    var commentdataid = $(this).attr("data-id") 
    $("#comment-modal").modal()//add btn here, inc ajax on btn
    $('#yes').click(function(){
       $.ajax({
        type: "POST",
        url: '/blog/' + (commentdataid) + '/deletecomment',
        success: function () {
          location.reload();
        },
        error: function (e) {
          //err
        }
      });
    })
  });

   //call delete post handler 
    $('#delete-btn').click(function () {
    var post = this
    //get the comment id from the icon id
    var postdataid = $(this).attr("data-id") 
    $("#delete-post-modal").modal()//add btn here, inc ajax on btn
    $('#post-yes').click(function(){
       $.ajax({
        type: "POST",
        url: '/blog/' + (postdataid) + '/deletepost',
        success: function () {
        window.location.replace("/blog");
        },
        error: function (e) {
          //err
        }
      });
    })
  });