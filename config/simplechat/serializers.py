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


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ['text', 'thread', 'sender']
        write_only = 'thread'
