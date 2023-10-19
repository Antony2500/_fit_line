from django.db import models

CATEGORY_CHOICES = (
    ('Протеїн', 'Protein Протеин Протеїн'),

    ('Гейнер', 'Weight Gainers Weight Gain Weight Increase Weight Building Весовое увеличение \
            Вагітність збільшується Гейнер Гейнер'),

    ('Амінокислоти та BCAAs', 'Amino Acids and BCAAs Amino Acids BCAAs Aminos Аминокислоты и BCAAs \
            Амінокислоти та BCAAs Аминокислоты Амінокислоти BCAA BCAA'),

    ('Креатин', 'Creatine Креатин Креатин'),

    ('Жироспалювачі', 'Fat Burners Fat Burn Fat Loss Fat Reduction Жиросжигатели Жироспалювачі \
            Втрата жиру Зменшення жиру'),

    ('Вітаміни та мінерали', 'Vitamins and Minerals Vitamins Minerals Vitamins & Minerals Витамины и минералы \
            Вітаміни та мінерали Витамины Вітаміни Минералы Мінерали'),

    ('Спортивне обладнання', 'Sports Equipment Equipment Training Gear Спортивное оборудование \
            Спортивне обладнання Оборудование для тренировок Обладнання для тренувань \
            Оборудование Обладнання Спортивный инвентарь Спортивний інвентар'),

    ('Замінник харчування', 'Food substitute Замінник харчування Заменитель питания'),

    ('Аксесуари для спорту', 'Sports Accessories Accessories Sports Gear Аксессуары для спорта \
            Аксесуари для спорту Спортивные принадлежности'),

    ('Легінси та штани', 'Leggings and Pants Leggings Pants Bottoms Леггинсы и штаны Легінси та штани \
            Леггинсы Легінси Штаны Штани Лосины Лосіни'),

    ('Верхній одяг', 'Tops and T-Shirts Tops T-Shirts Upperwear Верхняя одежда Верхній одяг \
            Футболки и майки Футболки та майки Футболки Футболки Майки Майки Топы Топи'),

    ('Шорти та Велосипедки', 'Shorts Шорты Шорти Велосипедки Велосипедки'),
)


class Product(models.Model):
    name = models.CharField(max_length=100, default='')
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    description = models.TextField(default='')
    composition = models.TextField(default='')
    prodapp = models.TextField(default='')
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=25, default='')

    manufacturer = models.CharField(max_length=20, default='')
    product_image = models.ImageField(upload_to='product', default='default_image.jpg')

    def __str__(self):
        return self.name
