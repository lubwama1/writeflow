
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, Comment
from .forms import CreatePostForm, CommentForm, ContactForm
from django.contrib import messages
import json
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from urllib.parse import unquote
from users.models import Profile
from notifications.signals import notify 
from notifications.models import Notification
from django.contrib.auth.models import User 
from django.contrib.contenttypes.models import ContentType
@login_required(login_url='account_login')
def home(request):

    posts = Post.objects.all().order_by('-created_at')

    # Pagination for posts
    paginated_by = Paginator(posts, 3)
    page_number = request.GET.get('page')
    try:
        # Get page objects
        page_obj = paginated_by.get_page(page_number)

        post_with_author = []
        for post in page_obj:
            profile = Profile.objects.filter(user=post.author).first()
            full_name = f'{profile.user.first_name} {profile.user.last_name}' if profile else None
            post_with_author.append({'post', post, 'full_name', full_name})
    except PageNotAnInteger:
        # If the page number is not an integer, show the first page
        page_obj = paginated_by.page(1)
    except EmptyPage:
        # If the page number is out of range, show the last page
        page_obj = paginated_by.page(paginated_by.num_pages)
       

    context = {
        'posts': page_obj,
        'page_obj': page_obj,
        'post_with_author': post_with_author,

    }
    return render(request, 'sphere/home.html', context)


@login_required(login_url='account_login')
def create_post(request):
    posts = Post.objects.all()
    if request.method == 'POST':
        form = CreatePostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            notify.send(
            sender=request.user, recipient=post.author,
            verb=f'{post.author} new post',
            action_object=post,
            description=f'{post.author.username} has a new post: {post.content[:100]}...', target=post)
            print(f"Notification sent to {post.author} from {request.user}") 
            return redirect('sphere:home')
        else:
            messages.error(request, 'Error creating post')
            return redirect('sphere:create-post')
    else:
        form = CreatePostForm()
    context = {'form': form, 'posts': posts}
    return render(request, 'sphere/create-post.html', context)


@login_required(login_url='account_login')
def update_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author:
        messages.error(request, 'You are not authorized to update this post')
        return redirect('sphere:home')
    if request.method == 'POST':
        form = CreatePostForm(request.POST, instance=post)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            messages.success(request, 'Post updated successfully')
            return redirect('sphere:home')
        else:
            messages.error(request, 'Failed to update post')
    else:
        form = CreatePostForm(instance=post)
    context = {
        'form': form,
    }
    return render(request, 'sphere/update-post.html', context)


@login_required(login_url='account_login')
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user == post.author:
        post.delete()
        messages.success(request, 'Post deleted successfully')
        return redirect('sphere:home')
    else:
        messages.error(request, 'Post failed to be deleted successfully')


@login_required(login_url='account_login')
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    profile = Profile.objects.filter(user=post.author).first()
    # profile_image = Profile.objects.filter(user=request.user).first() #if request.user.is_authenticated else None
    # profile_image = profile
    author = request.user 
    profile_image = Profile.objects.filter(user=author)
    full_name = f'{profile.user.first_name} {profile.user.last_name}' if profile else None
    comments = Comment.objects.filter(post=post, parent__isnull=True)
    comment_form = CommentForm()
    # comments_with_profiles = []
    # for comment in comments:
    #     profile = Profile.objects.filter(user=comment.author)
    #     comments_with_profiles.append({'comment': comment, 'profile': profile})
    # print(comments_with_profiles)    
    if request.method == 'POST':
        if request.headers.get('Content-Type') == 'application/json':
            # if request.content_type == 'application/json':

            body = json.loads(request.body)
            # For Post Like/Unlike
            if body.get('action') == 'toggle_like':
                if request.user in post.likes.all():
                    post.likes.remove(request.user)
                    liked = False
                else:
                    post.likes.add(request.user)
                    liked = True
                    notify.send(sender=request.user, recipient=post.author, verb=f"{request.user} liked your post", target=post, description=post.title, action_object=post)
                return JsonResponse({'success': True, 'liked': liked, 'likes': post.likes.count()})

            # For Comment Like/Unlike
            if body.get('action') == 'toggle_comment_like':
                comment_id = body.get('comment_id')
                comment = get_object_or_404(Comment, pk=comment_id)
                if request.user in comment.likes.all(): 
                    comment.likes.remove(request.user)
                    liked = False
                else:
                    comment.likes.add(request.user)
                    liked = True
                    notify.send(
                        sender=request.user, recipient=comment.author, verb=f"{request.user} liked your comment",target=comment, description=comment.content[:20], action_object=comment
                    )
                return JsonResponse({'success': True, 'liked': liked, 'likes': comment.likes.count()})

        # comment submission
        # Handle comment form submission
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            parent_comment_id = request.POST.get('parent_comment_id')
            if parent_comment_id:
                comment.parent = Comment.objects.get(id=parent_comment_id)
            comment.save()
            return redirect('sphere:post-detail', pk=pk)
        
        content = request.POST.get('content')
        comment = Comment.objects.create(post=post, author=request.user, content=content)
        post_not = comment.author
        post_owner = post.author
        user = User.objects.get(user=request.user)  # replace with actual user
        # target_user = User.objects.get(user=request.user)  # replace with actual target user
        actor_content_type = ContentType.objects.get_for_model(user)
        notify.send(
        sender=comment.author, recipient=post_owner,
        verb='commented on your post',
        action_object=comment,
        description=f'{comment.user.username} commented: {comment.content[:100]}...', target=post, actor_content_type=actor_content_type, actor_object_id=user.id)

    context = {
        'post': post,
        'likes': post.likes.count(),
        'comment_form': comment_form,
        'comments': comments,
        # 'comment_likes': comments.likes.count(),
        'full_name': full_name,
        'profile': profile_image
        # 'comments_with_profiles': comments_with_profiles,
    }
    return render(request, 'sphere/post-detail.html', context)


@login_required(login_url='account_login')
def about_page(request):
    return render(request, 'sphere/about.html')


@login_required(login_url='account_login')
def contact_page(request):
    return render(request, 'sphere/contact.html')


@login_required(login_url='account_login')
def contact_page(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Thank you for contacting us! We'll get back to you soon.")
            return redirect('sphere:home')
    else:
        form = ContactForm()

    return render(request, 'sphere/contact.html', {'form': form})


def perform_search(query):
    posts = Post.objects.filter(Q(published=True))
    if query:
        posts = posts.filter(Q(author__username__icontains=query)
                             | Q(title__icontains=query))
    return posts


@login_required(login_url='account_login')
def search_post(request):
    query = request.GET.get('query', '')
    query = unquote(query)
    print(f"Search Query: {query}")
    posts = perform_search(query)
    paginator = Paginator(posts, 2)  # Show 10 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    print(f"Request object: {type(request)}")

    context = {
        'posts': page_obj,
        'query': query,
        'is_search_page': True,
    }
    return render(request, 'sphere/search-post.html', context)
@login_required(login_url='account_login')
def reply_comment(request, pk):
    # Fetch the parent comment and its replies
    comment = get_object_or_404(Comment, pk=pk)
    replies = comment.replies.all()

    # Initialize the comment form
    comment_form = CommentForm(request.POST or None)

    if request.method == 'POST' and comment_form.is_valid():
        # Handle reply form submission, create a new reply
        new_reply = comment_form.save(commit=False)
        new_reply.parent = comment
        new_reply.author = request.user
        new_reply.post = comment.post
        new_reply.save()

        # Ensure the comment has an author before sending notification
        comment_owner = comment.author
        if comment_owner:
            print(f"Sending notification to {comment_owner}")  # Debugging
            notify.send(
                sender=request.user,
                recipient=comment_owner,
                verb=f"{request.user} replied on your comment",
                target=comment,
                description=comment.content[:20],
                action_object=new_reply
            )

    return render(request, 'sphere/reply.html', {
        'comment': comment,
        'replies': replies,
        'comment_form': comment_form,
    })

@login_required(login_url='account_login')
def notification_view(request):
    notifications = Notification.objects.filter(recipient=request.user, unread=True).order_by('-timestamp')

    # Paginate: Show only 4 notifications at a time
    paginated_by = Paginator(notifications, 2)  # Show 4 notifications per page
    page_number = request.GET.get('page')
    try:
        page_obj = paginated_by.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginated_by.page(1)
    except EmptyPage:
        page_obj = paginated_by.page(paginated_by.num_pages)    
    # Add notification URLs dynamically
    for notification in page_obj:
        if hasattr(notification.target, 'post'):  
            notification_url = notification.target.post.get_absolute_url() + f"#comment-{notification.target.pk}"
        elif hasattr(notification.target, 'get_absolute_url'):
            notification_url = notification.target.get_absolute_url()
        else:
            notification_url = "#"  

        notification.notification_url = notification_url

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # Handle AJAX request
        notifications_data = [
            {
                "verb": n.verb,
                "description": n.description,
                "timestamp": n.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "notification_url": n.notification_url
            } for n in page_obj
        ]
        return JsonResponse({"notifications": notifications_data, "has_next": page_obj.has_next()}) 

    return render(request, 'sphere/notifications_list.html', {'notifications': page_obj, 'page_obj': page_obj})

def react_to_post(request, post_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            emoji = data.get("emoji")

            post = Post.objects.get(id=post_id)
            
            # Here, you need a model to track reactions (e.g., PostReaction)
            post, created = Post.objects.get_or_create(user=request.user, post=post, emoji=emoji)
            
            if not created:
                post.reactions.delete()  # Toggle reaction (remove if already reacted)
                reaction_count = Post.objects.filter(post=post, emoji=emoji).count()
                return JsonResponse({"success": True, "reaction_count": reaction_count})
            
            reaction_count = Post.objects.filter(post=post, emoji=emoji).count()
            return JsonResponse({"success": True, "reaction_count": reaction_count})

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    
    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)

