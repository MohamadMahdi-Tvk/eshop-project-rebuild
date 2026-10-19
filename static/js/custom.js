function sendArticleComment() {
    var comment = $('#commentText').val();

    $.get('/articles/add_article_comment', {
        articleComment: comment,
        articleId: 30,
        parentId: null
    }).then(res => {
        console.log(res)
    });
}