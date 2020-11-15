from uuid import UUID

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import DestroyAPIView, CreateAPIView, ListAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from simplechat import serializers
from simplechat.models import Thread, Message
from users.models import User


class CreateDestroyThread(CreateAPIView, DestroyAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = serializers.CreateRetrieveThreadSerializer

    def validate(self):
        if 'participants' not in self.request.data:
            raise ValidationError({"error": "participants"})
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
    serializer_class = serializers.MessageSerializer
    lookup_field = 'thread__id__in'
    queryset = Message.objects.all()

    def get(self, request, *args, **kwargs):
        self.validate(kwargs['pk'])
        return super(GetCreateMessages, self).get(request, args, kwargs)

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
