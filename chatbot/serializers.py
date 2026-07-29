
from rest_framework import serializers
from .models import UploadFile

class UploadFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadFile
        fields = ['id', 'title', 'file', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_at']



from rest_framework import serializers
from .models import UploadRecord

class UploadRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadRecord
        fields = "__all__"

from .models import AdminVideo

class AdminVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminVideo
        fields = ['id', 'url', 'created_at']
