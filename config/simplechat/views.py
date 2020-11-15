from uuid import UUID

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import DestroyAPIView, CreateAPIView, ListAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from simplechat import serializers
from simplechat.models import Thread, Message
from users.models import User


class CreateDestroyThread(CreateAPIView, DestroyAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = serializers.CreateRetrieveThreadSerializer

    def validate(self):
        if 'participants' not in self.request.data:
            raise ValidationError({"error": "Participants not set"})
        participants = self.request.data['participants']
        if not isinstance(participants, list):
            raise ValidationError({"error": "Participants should be a list of ids"})
        if len(participants) != 2:
            raise ValidationError({"error": "Participants should be exact 2"})
        if not all([isinstance(user_id, str) for user_id in participants]):
            raise ValidationError({"error": "Participants should be exact 2"})
        try:
            [UUID(user_id) for user_id in participants]
        except ValueError:
            raise ValidationError({"error": "Not valid values of users' ids."})
        if not User.objects.filter(id=participants[0]).exists():
            raise ValidationError({"error": f"User with id {participants[0]} doesn't exist."})
        if not User.objects.filter(id=participants[1]).exists():
            raise ValidationError({"error": f"User with id {participants[0]} doesn't exist."})

    def create(self, request, *args, **kwargs):
        self.validate()
        try:
            users = User.objects.filter(id__in=request.data['participants'])
            first_user_filter = Thread.objects.filter(participants__id=users[0].id)
            second_user_filter = Thread.objects.filter(participants__id=users[1].id)
            thread = (first_user_filter & second_user_filter).first()
            return Response(data=serializers.ListThreadSerializer(thread).data, status=status.HTTP_200_OK)
        except Thread.DoesNotExist:
            return super(CreateDestroyThread, self).create(request, args, kwargs)


class ListUsersThreads(ListAPIView):
    def validate(self, user_pk):
        if not User.objects.filter(id=user_pk).exists():
            raise ValidationError({"error": f"User with id {user_pk} doesn't exist."})

    permission_classes = [IsAuthenticated]
    serializer_class = serializers.ListThreadSerializer
    lookup_field = 'participants__id'
    queryset = Thread.objects.all()

    def get(self, request, *args, **kwargs):
        self.validate(kwargs['pk'])
        return super(ListUsersThreads, self).get(request, args, kwargs)


class GetCreateMessages(ListCreateAPIView):

    def validate(self, thread_pk):
        if not Thread.objects.filter(id=thread_pk).exists():
            raise ValidationError({"error": f"Thread with id {thread_pk} doesn't exist."})
        if self.request.method == "POST":
            if 'sender' not in self.request.data:
                raise ValidationError(
                    {"error": f"sender should be set in data"}
                )
            if 'text' not in self.request.data:
                raise ValidationError(
                    {"error": f"sender should be set in data"}
                )
            if not Thread.objects.filter(pk=thread_pk,
                                         participants__id=self.request.data['sender']).exists():
                raise ValidationError(
                    {"error": f"User with id {self.request.data['sender']} doesn't have access to this thread."}
                )

    permission_classes = [IsAuthenticated]
    serializer_class = serializers.CreateMessageSerializer
    lookup_field = 'thread__id__in'
    queryset = Message.objects.all()

    def list(self, request, *args, **kwargs):
        self.validate(kwargs['pk'])
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = serializers.DisplayMessageSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = serializers.DisplayMessageSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        thread_id = kwargs['pk']
        self.validate(thread_id)
        data = request.data
        data['thread'] = thread_id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UsersMessagesCount(APIView):

    permission_classes = [IsAuthenticated]

    def validate(self, user_pk):
        if not User.objects.filter(id=user_pk).exists():
            raise ValidationError({"error": f"User with id {user_pk} doesn't exist."})

    def get(self, request, *args, **kwargs):
        user_pk = kwargs['pk']
        self.validate(user_pk)
        messages = Message.objects.filter(thread__participants__id=user_pk).exclude(sender_id=user_pk)
        is_read = request.query_params.get('is_read', None)
        if is_read == 'true':
            messages = messages.filter(is_read=True)
        if is_read == 'false':
            messages = messages.filter(is_read=False)
        content = {'messages_count': messages.count()}
        return Response(data=content, status=status.HTTP_200_OK)


class MarkMessagesRead(APIView):

    permission_classes = [IsAuthenticated]

    def validate(self, user_pk):
        if not User.objects.filter(id=user_pk).exists():
            raise ValidationError({"error": f"User with id {user_pk} doesn't exist."})
        if self.request.method == 'POST':
            if 'messages' not in self.request.data:
                raise ValidationError({"error": "Messages not set"})
            messages = self.request.data['messages']
            try:
                [UUID(message_id) for message_id in messages]
            except ValueError:
                raise ValidationError({"error": "Not valid values of messages' ids."})
            if len(messages) != Message.objects.filter(
                    id__in=messages,
                    thread__participants__id=user_pk
            ).exclude(sender_id=user_pk).count():
                raise ValidationError({"error": f"Not all messages related to current user."})

    def post(self, request, *args, **kwargs):
        user_pk = kwargs['pk']
        import ipdb
        ipdb.set_trace()
        self.validate(user_pk)
        messages = Message.objects.filter(id__in=request.data['messages'])
        for message in messages:
            message.is_read = True
        Message.objects.bulk_update(messages, ['is_read'])
        serialized = serializers.DisplayMessageSerializer(messages, many=True)
        return Response(data=serialized.data, status=status.HTTP_200_OK)
