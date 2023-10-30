from catalog.models import Image
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

# Получите все существующие объекты Image
images = Image.objects.all()

