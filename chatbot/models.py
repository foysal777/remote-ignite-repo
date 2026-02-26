
from django.db import models
from django.conf import settings
class UploadFile(models.Model):
    title = models.CharField(max_length=255, blank=True)
    file = models.FileField(upload_to='uploads/%Y/%m/%d/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title or self.file.name



from django.db import models

class UploadRecord(models.Model):
    ROLE_CHOICES = (("admin","admin"), ("user","user"))
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="user")
    original_name = models.CharField(max_length=255)
    s3_key = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default="pending") 
    error = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=100, null=True, blank=True)


    def __str__(self):
        return f"{self.original_name} - {self.status}"




class ChatSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    conversation_id = models.CharField(max_length=128, db_index=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)





class QueryHistory(models.Model):
    

    chat_session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name="messages" , null=True, blank=True )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE , null=True, blank=True )
    query = models.TextField()
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.created_at}"
    



from django.db import models

class ProcessedStripeEvent(models.Model):
    stripe_event_id = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)


class ProcessedStripeInvoice(models.Model):
    stripe_invoice_id = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)



class VoiceConversationHistory(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="voice_histories"
    )

    chat_session = models.ForeignKey(
        "ChatSession",
        on_delete=models.CASCADE,
        related_name="voice_messages"
    )

    conversation_id = models.CharField(
        max_length=128,
        db_index=True,
        null=True,
        blank=True
    )

    user_text = models.TextField()          # transcription
    answer_text = models.TextField()        # AI response

    voice_id = models.CharField(
        max_length=64,
        null=True,
        blank=True
    )

    presigned_url = models.URLField(
        null=True,
        blank=True
    )

    s3_key = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.user.email} - {self.created_at}"