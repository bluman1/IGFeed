from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from IGFeedAPI.models import User
from IGFeedAPI.retriever import get_latest_image
from IGFeedAPI.serializers import UserSerializer


@csrf_exempt
@api_view(['GET'])
def list_users(request):
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# POST: {"user_name": "_bluman", "feed_name": "wisdomfeed"} DELETE: {"user_name: "_bluman"}
@csrf_exempt
@api_view(['POST', 'DELETE'])
def user_ops(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        data = dict(request.data)
        name = data['user_name']
        user = User.objects.get(user_name=name)
        serializer = UserSerializer(user)
        User.objects.get(user_name=name).delete()
        return Response(serializer.data, status=status.HTTP_200_OK)


# {"user_name": "_bluman", "feed_name": "wisdomfeed"}
@csrf_exempt
@api_view(['POST'])
def set_user_feed(request):
    if request.method == 'POST':
        data = dict(request.data)
        name = data['user_name']
        feed_name = data['feed_name']
        user = User.objects.get(user_name=name)
        user.feed_name = feed_name
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


# {"user_name": "_bluman"}
@csrf_exempt
@api_view(['POST'])
def get_latest(request):
    if request.method == 'POST':
        data = dict(request.data)
        name = data['user_name']
        user = User.objects.get(user_name=name)
        feed_name = user.feed_name
        latest_image = get_latest_image(feed_name)
        return HttpResponse(latest_image, content_type="image/jpg", status=status.HTTP_200_OK)
