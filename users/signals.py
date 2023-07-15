from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


#! bu signali bir user oluşturulduktan (register edildikten hemen) sonra Token da oluşturması yani otomatik login olması için kullandık. Bana user bilgisi ile birlikte Token'ın da dönmesi için views.py'da RegisterApi'nin create metodunu override ettik.

@receiver(post_save, sender=User)
def create_Token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
