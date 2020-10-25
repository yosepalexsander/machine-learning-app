from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes
from rest_framework import status

from .models import Post
from .serializers import PostSerializer


@api_view(["GET", "POST", "DELETE"])
@parser_classes([JSONParser])
def post_list(request):
    """
    Returns a list of all created posts
    """
    if request.method == "GET":
        posts = Post.objects.all()
        title = request.query_params.get("title", None)
        if title is not None:
            posts = posts.filter(title__icontains=title)

        posts_serializer = PostSerializer(posts, many=True)
        return Response(posts_serializer.data, status=status.HTTP_200_OK)

    elif request.method == "POST":
        post_data = request.data
        post_serializer = PostSerializer(data=post_data)
        if post_serializer.is_valid():
            post_serializer.save()
            return Response(post_serializer.data, status=status.HTTP_201_CREATED)
        return Response(post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        total_deleted = Post.objects.all().delete()
        return Response(
            {"message": f"{total_deleted[0]} Posts were deleted successfully!"},
            status.HTTP_204_NO_CONTENT,
        )


@api_view(["GET", "PUT", "DELETE"])
@parser_classes([JSONParser])
def post_detail(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response(
            {"message": "The post does not exist"}, status=status.HTTP_404_NOT_FOUND
        )

    if request.method == "GET":
        post_serializer = PostSerializer(post)
        return Response(post_serializer.data, status=status.HTTP_200_OK)

    elif request.method == "PUT":
        post_data = request.data
        post_serializer = PostSerializer(post_data, data=post_data)
        if post_serializer.is_valid():
            post_serializer.save()
            return Response(post_serializer)
        return Response(post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        post.delete()
        return Response({"message": "Post was deleted succesfully"})
