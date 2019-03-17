from django.db import models
from django.utils.translation import gettext_lazy as _


class Book(models.Model):
    authors = models.ManyToManyField("Author", related_name="books")
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    paper_book = models.OneToOneField("PaperBook", blank=True, null=True, on_delete=models.SET_NULL)
    ebook = models.OneToOneField("Ebook", blank=True, null=True, on_delete=models.SET_NULL)
    audio_book = models.OneToOneField("AudioBook", blank=True, null=True, on_delete=models.SET_NULL)    

    series = models.ForeignKey("Series", on_delete=models.CASCADE, related_name="books", blank=True, null=True)
    cover_photo = models.ImageField(upload_to="Books", null=True, blank=True)

    category = models.ForeignKey("Category", on_delete=models.SET_NULL, blank=True, null=True)
    tags = models.ManyToManyField("Tag", related_name="books", blank=True)

    def __str__(self):
        return f'{self.title}'


class Series(models.Model):
    title = models.CharField(max_length=40)
    
    
class PaperBook(models.Model):
    price = models.DecimalField(decimal_places=2, max_digits=10)
    
    cover_type = (
        ("HARD", "Hard"),
        ("SOFT", "Soft"),
        )
    cover = models.CharField(choices=cover_type, max_length=4)


class EBook(models.Model):
    price = models.DecimalField(decimal_places=2, max_digits=10)
    formats = (
        ("PDB", "pdb"),
        ("EPUB", "epub"),
        ("PDF", "pdf"), 
        ("AZW", "azw"),
        ("IBOOKS", "ibooks"),
        ) 
    aveiable_format = models.CharField(choices=formats, max_length=6)


class AudioBook(models.Model):
    price = models.DecimalField(decimal_places=2, max_digits=10)
    reader = models.ManyToManyField("Reader", )
    


class Person(models.Model):
    first_name = models.CharField(max_length=30, blank=True)
    second_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    
    def __str__(self):
        if(self.second_name):
            return f'{self.first_name} {self.second_name} {sefl.last_name}'
        return f'{self.first_name} {self.last_name}'
        
    class Meta:
        abstract = True


class Author(Person):
    avatar = models.ImageField(upload_to="Books", null=True, blank=True)
    description = models.TextField(null=True, blank=True)


class Reader(Person):
    pass

    def __str__(self):
        return f'{self.first_name} {self.second_name} {self.last_name}'

    
class Tag(models.Model):
    text = models.CharField(max_length = 40)
    
    def __str__(self):
        return self.text


class Category(models.Model):
    text = models.CharField(max_length = 40)

    def __str__(self):
        return self.text


class Order(models.Model):
    email = models.EmailField(_('email adress'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    
    creation_date = models.DateTimeField(blank=True, null=True)    

    house_number = models.CharField(max_length=12, blank=True, null=True)
    street = models.CharField(max_length=30, blank=True, null=True)
    city = models.CharField(max_length=30, blank=True, null=True)
    zip_code = models.CharField(max_length=10, blank=True, null=True)
    voivodeship = models.CharField(max_length=30, blank=True, null=True)
    additional_info = models.CharField(max_length=200, blank=True, null=True)


    paid = models.BooleanField(default=False)
    paid_date = models.DateTimeField(blank=True, null=True)


class OrderItem(models.Model):

    order = models.ForeignKey("Order", on_delete=models.CASCADE)
    book = models.ForeignKey("Book", on_delete=models.CASCADE)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    quantity = models.PositiveIntegerField(default=1)