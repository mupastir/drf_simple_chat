from rest_framework import serializers

from simplechat.models import Thread


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
        return thread.message_set.last()
