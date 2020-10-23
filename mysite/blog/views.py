from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework import status

from .models import Post
from .serializers import PostSerializer


@api_view(["GET", "POST", "DELETE"])
def post_list(request):
    if request.method == "GET":
        posts = Post.objects.all()
        title = request.query_params.get("title", None)
        if title is not None:
            posts = posts.filter(title__icontains=title)

        posts_serializer = PostSerializer(posts, many=True)
        return JsonResponse(posts_serializer.data, safe=False)

    elif request.method == "POST":
        post_data = JSONParser().parse(request)
        post_serializer = PostSerializer(data=post_data)
        if post_serializer.is_valid():
            post_serializer.save()
            return JsonResponse(post_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        total_deleted = Post.objects.all().delete()
        return JsonResponse(
            {"message": f"{total_deleted[0]} Posts were deleted successfully!"},
            status.HTTP_204_NO_CONTENT,
        )


@api_view(["GET", "PUT"])
def post_detail(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return JsonResponse(
            {"message": "The post does not exist"}, status=status.HTTP_404_NOT_FOUND
        )

    if request.method == "GET":
        post_serializer = PostSerializer(post)
        return JsonResponse(post_serializer.data)

    elif request.method == "PUT":
        post_data = JSONParser().parse(request)
        post_serializer = PostSerializer(post_data, data=post_data)
        if post_serializer.is_valid():
            post_serializer.save()
            return JsonResponse(post_serializer)
        return JsonResponse(post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        post.delete()
        return JsonResponse({"message": "Post was deleted succesfully"})
