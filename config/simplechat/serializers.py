from rest_framework import serializers

from simplechat.models import Thread, Message


class CreateRetrieveThreadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Thread
        fields = ['participants']


class ListThreadSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Thread
        fields = ['id', 'participants', 'last_message']

    def get_last_message(self, thread):
        return str(thread.message_set.last())


class DisplayMessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ['id', 'text', 'thread', 'sender', 'created', 'is_read']


class CreateMessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ['text', 'sender', 'thread']
