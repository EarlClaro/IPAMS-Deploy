from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from langchain_community.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain_openai import OpenAI
import os
import time
from django.http import JsonResponse
from rest_framework.decorators import api_view
import json
from .models import researchpaper, Thread, Message, User
from .serializers import ThreadCreateSerializer
from rest_framework import generics, status
from .serializers import ThreadSerializer, MessageSerializer, UserCreateSerializer, UserLoginSerializer, UserSerializer, UserUpdateSerializer
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
from django.core.paginator import Paginator

#ipams
from concurrent.futures import thread
from http.client import INTERNAL_SERVER_ERROR
import json
from threading import Thread
import requests

from django.contrib import messages
from django.contrib.auth import signals, authenticate, login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.shortcuts import redirect

from ipams import settings
from . import forms
from .decorators import authorized_roles
from .models import User, UserRole, RoleRequest, Course, Student, Log, Setting, College, Department, Adviser, UserRecord
from records.models import CheckedRecord, Record, RecordUpload, CheckedUpload
from notifications.models import Notification, NotificationType
from accounts.auxfunctions import EmailThreading, roleRequestStudent, roleRequestAdviser
from django.db.models import Q, Subquery
from django.contrib.auth.hashers import check_password

os.environ["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY")
# Create the SQLDatabase instance with the MySQL connection URI
db = SQLDatabase.from_uri(f"mysql://{settings.DATABASES['default']['USER']}:{settings.DATABASES['default']['PASSWORD']}@{settings.DATABASES['default']['HOST']}:{settings.DATABASES['default']['PORT']}/{settings.DATABASES['default']['NAME']}", include_tables=[])

llm = OpenAI(temperature=0, verbose=True)

db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)


# Admin views
@csrf_exempt
def upload_and_replace_data(request):
    if 'file' in request.FILES:
        uploaded_file = request.FILES['file']
        if uploaded_file.name.endswith('.json'):
            try:
                with uploaded_file.open() as file:
                    data = json.load(file)

                    # Clear existing data
                    researchpaper.objects.all().delete()

                    # Insert new data from the JSON file
                    total_rows = len(data)
                    chunk_size = 100
                    for i in range(0, total_rows, chunk_size):
                        chunk_data = data[i:i+chunk_size]
                        for item in chunk_data:
                            # Extract code and description from 'record_type' value
                            record_type_value = item.get('Record Type \n(1 - Proposal, 2 - Thesis/Research, 3 - Project)', '')
                            code, _ = record_type_value.split('-', 1)  # Split at the first dash
                            code = code.strip()

                            # Create the ResearchPaper object using the extracted code
                            researchpaper.objects.create(
                                title=item['Title'],
                                abstract=item['Abstract'],
                                year=item['Year'],
                                record_type_id=None,  # Adjust based on your data source
                                adviser_id=None,  # Adjust based on your data source
                                classification_id=item['Classification \n(1 - Basic Research, 2 - Applied Research)\\'],
                                representative=item['Representative'],  # Adjust based on your data source
                                year_accomplished=item['Year Accomplished'],  # Adjust based on your data source
                                year_completed=item.get('Year Completed'),  # Adjust based on your data source
                                is_ip=item.get('Is IP'),  # Adjust based on your data source
                                for_commercialization=item.get('For Commercialization'),  # Adjust based on your data source
                                date_created=item.get('Date Created'),  # Adjust based on your data source
                                is_marked=item.get('Is Marked'),  # Adjust based on your data source
                            )
                        progress = int((i + chunk_size) / total_rows * 100)
                        if progress % 20 == 0:  # Send progress update every 20%
                            return JsonResponse({'progress': progress})

                    return JsonResponse({'message': 'Data replaced successfully.'})
            except Exception as e:
                return JsonResponse({'error': f'An error occurred while processing the file: {str(e)}'}, status=400)
        else:
            return JsonResponse({'error': 'Invalid file type. Only JSON files are accepted.'}, status=400)
    else:
        return JsonResponse({'error': 'No file provided in the request.'}, status=400)
    

# Thread Views (CRUD)
class ThreadListCreateView(generics.ListCreateAPIView):
    queryset = Thread.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ThreadCreateSerializer
        return ThreadSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"message": "Thread created", "data": serializer.data}, status=status.HTTP_201_CREATED, headers=headers)

class ThreadDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"message": "Thread updated", "data": serializer.data})

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Thread deleted"}, status=status.HTTP_204_NO_CONTENT)

class DeleteAllThreads(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        # Delete all threads associated with the user making the request
        Thread.objects.filter(user=request.user).delete()
        return Response({"message": "All threads deleted for the current user"}, status=status.HTTP_204_NO_CONTENT)

class UserThreadListView(generics.ListAPIView):
    serializer_class = ThreadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Retrieve the authenticated user based on the token
        user = self.request.user
        
        # Filter threads associated with the authenticated user
        queryset = Thread.objects.filter(user=user)
        return queryset

class MessageCreateView(generics.CreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        thread_id = request.data.get("thread_id")
        thread = get_object_or_404(Thread, pk=thread_id)

        query = request.data.get("query")

        # Fetch conversation history
        conversation_history = Message.objects.filter(thread=thread).order_by('created_at')
        history_text = "\n".join([json.loads(msg.message_text)['query'] + "\n" + json.loads(msg.message_text)['response'] for msg in conversation_history])

        # Combine history with the current query
        combined_query = history_text + "\nUser: " + query  # Make sure to label the speaker for clarity

        # Debug: print combined_query to check if history is correct
        print("Combined Query for db_chain:", combined_query)

        # Call db_chain with the combined_query to consider past conversation
        response = db_chain(combined_query)  # Assuming db_chain can handle this format

        # Debug: print response to check what db_chain returns
        print("Response from db_chain:", response)

        # Create a mutable copy of request.data
        mutable_data = request.data.copy()

        # Add the thread and message_text to the mutable_data
        mutable_data["thread"] = thread.pk

        # Structure the message_text for easy mapping in React
        message_text = {
            'query': query,
            'response': response.get("result", "No result found")
        }

        # Set the message_text field with the structured data
        mutable_data["message_text"] = json.dumps(message_text)

        serializer = self.get_serializer(data=mutable_data)
        serializer.is_valid(raise_exception=True)

        # Save the new message
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response({"message": "Message created", "data": serializer.data}, status=status.HTTP_201_CREATED, headers=headers)


class MessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Get the thread_id from the URL parameter
        thread_id = self.kwargs.get('thread_id')
        
        # Retrieve all messages associated with the specified thread
        queryset = Message.objects.filter(thread_id=thread_id)
        return queryset

class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        email = request.data.get('email', None)

        if email:
            if User.objects.filter(email=email).exists():
                # Email is already in use
                return Response({'error': 'Email is already in use.'}, status=status.HTTP_409_CONFLICT)

            serializer = self.get_serializer(data=request.data)
            try:
                serializer.is_valid(raise_exception=True)
            except serializers.ValidationError as validation_error:
                # Improper email format
                return Response({'error': 'Invalid email format.', 'details': validation_error.detail}, status=status.HTTP_400_BAD_REQUEST)

            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        # Invalid request, email is required
        return Response({'error': 'Email is required.'}, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        permission_classes = [AllowAny]

        user = serializer.validated_data['user']

        user = serializer.validated_data['user']
        user = serializer.validated_data['user']
        
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        response_data = {
            'message': 'Login successful',
            'email': user.email,
            'name': user.name,
            'access_token': access_token,
            'is_superuser': serializer.validated_data['is_superuser'],
        }
        
        return Response(response_data, status=status.HTTP_200_OK)

class UserUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        user = request.user  # Get the currently logged-in user

        serializer = UserUpdateSerializer(instance=user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserDetailsView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user 