# author: zachary paulson
import datetime

def create_draft_post(posts, blog_id, content):
    new_post = posts.insert(blogId=blog_id, body=content)
    return new_post.execute()

def update_blog_post(posts, blog_id, post_id, content):
    update_post = posts.update(blogId=blog_id, postId=post_id, body=content)
    return update_post.execute()

def content_setup(blog_id, title, body):
    today = datetime.date.today()

    content = {"kind": "blogger#post",
               "id": blog_id,
               "title": "{0}, {1}".format(title, today),
               "content": body}

    return content

def test_post(users, blogs, posts):
    # Retrieve this user's profile information
    this_user = users.get(userId='self').execute()
    print('This user\'s display name is: %s' % this_user['displayName'])

    # Retrieve the list of Blogs this user has write privileges on
    this_users_blogs = blogs.listByUser(userId='self').execute()
    for blog in this_users_blogs['items']:
        print('The blog named \'%s\' is at: %s' % (blog['name'], blog['url']))
        # Publish a draft page
        new_post = create_draft_post(blog['id'], posts)
        print(new_post)

    # List the posts for each blog this user has
    for blog in this_users_blogs['items']:
        print('The posts for %s:' % blog['name'])
        request = posts.list(blogId=blog['id'])
        print('The id is: %s' % blog['id'])
        while request != None:
            posts_doc = request.execute()
            if 'items' in posts_doc and not (posts_doc['items'] is None):
                for post in posts_doc['items']:
                    print('  %s (%s)' % (post['title'], post['url']))
            request = posts.list_next(request, posts_doc)
