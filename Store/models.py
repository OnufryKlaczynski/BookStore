from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.contrib.auth import get_user_model

User = get_user_model()

class Book(models.Model):
    authors = models.ManyToManyField("Author", related_name="books")
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    paper_book = models.OneToOneField("PaperBook", blank=True, null=True, on_delete=models.SET_NULL)
    ebook = models.OneToOneField("Ebook", blank=True, null=True, on_delete=models.SET_NULL)
    audio_book = models.OneToOneField("AudioBook", blank=True, null=True, on_delete=models.SET_NULL)    

    series = models.ForeignKey("Series", on_delete=models.CASCADE, related_name="books", blank=True, null=True)
    cover_photo = models.ImageField(upload_to="Books", null=True, blank=True)

    category = models.ForeignKey("Category", related_name="books", on_delete=models.SET_NULL, blank=True, null=True)
    tags = models.ManyToManyField("Tag", related_name="books", blank=True)

    slug = models.SlugField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Book, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.title}'

    
    @property
    def first_available_type(self):
        if self.paper_book:
            return self.paper_book 

        elif self.ebook:
            return self.ebook

        elif self.audio_book:
            return self.audio_book
            
        return None


class Series(models.Model):
    title = models.CharField(max_length=40)


class GenericBookType(models.Model):
    price = models.DecimalField(decimal_places=2, max_digits=10)

    @property
    def float_price(self):
        return float(self.price)


    class Meta:
        abstract = True

    
class PaperBook(GenericBookType):
    
    
    cover_type = (
        ("HARD", "Hard"),
        ("SOFT", "Soft"),
        )
    cover = models.CharField(choices=cover_type, max_length=4)

    def __str__(sefl):
        return "paper_book"



class EBook(GenericBookType):
    
    formats = (
        ("PDB", "pdb"),
        ("EPUB", "epub"),
        ("PDF", "pdf"), 
        ("AZW", "azw"),
        ("IBOOKS", "ibooks"),
        ) 
    aveiable_format = models.CharField(choices=formats, max_length=6)

    def __str__(self):
        return "ebook"


class AudioBook(GenericBookType):
    
    reader = models.ManyToManyField("Reader", )
    
    def __str__(self):
        return "audio_book"


class Person(models.Model):
    first_name = models.CharField(max_length=30, blank=True)
    second_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    
    def __str__(self):
        if(self.second_name):
            return f'{self.first_name} {self.second_name} {self.last_name}'
        return f'{self.first_name} {self.last_name}'
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.__str__())
        super(Person, self).save(*args, **kwargs)


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
    text = models.CharField(max_length = 40, unique=True)
    
    def __str__(self):
        return self.text

    def save(self, *args, **kwargs):
        self.slug = slugify(self.text)
        super(Tag, self).save(*args, **kwargs)


class Category(models.Model):
    text = models.CharField(max_length = 40, unique=True)

    def __str__(self):
        return self.text

    def save(self, *args, **kwargs):
        self.slug = slugify(self.text)
        super(Category, self).save(*args, **kwargs)


class Order(models.Model):
    email = models.EmailField(_('email adress'))
    first_name = models.CharField(_('first name'), max_length=30)
    last_name = models.CharField(_('last name'), max_length=30)
    
    creation_date = models.DateTimeField(auto_now=True, blank=True, null=True, )    

    house_number = models.CharField(max_length=12, )
    street = models.CharField(max_length=30, )
    city = models.CharField(max_length=30, )
    zip_code = models.CharField(max_length=10, )
    voivodeship = models.CharField(max_length=30, )
    additional_info = models.CharField(max_length=200, blank=True, null=True)


    paid = models.BooleanField(default=False)
    paid_date = models.DateTimeField(blank=True, null=True)

    user = models.ForeignKey(User, related_name="orders", blank=True, null=True, on_delete=models.SET_NULL, )


class OrderItem(models.Model):

    order = models.ForeignKey("Order", related_name="items", on_delete=models.CASCADE)
    book = models.ForeignKey("Book", on_delete=models.CASCADE)
    book_type = models.CharField(max_length=20)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    quantity = models.PositiveIntegerField(default=1)


    def __str__(self):
        return f'{self.book_type}, {self.book}, {self.price}, {self.quantity}'