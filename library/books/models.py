from django.db import models
from django_jalali.db import models as jmodels
from django.urls import reverse
from django.contrib.auth import get_user_model


countries = {
    "Afghanistan" : "AF","Albania" : "AL","Algeria" : "DZ","Andorra" : "AD","Angola" : "AO","Antigua and Barbuda" : "AG","Argentina" : "AR","Armenia" : "AM","Australia" : "AU","Austria" : "AT","Azerbaijan" : "AZ","Bahamas" : "BS","Bahrain" : "BH","Bangladesh" : "BD","Barbados" : "BB","Belarus" : "BY","Belgium" : "BE","Belize" : "BZ","Benin" : "BJ","Bhutan" : "BT","Bolivia (Plurinational State of)" : "BO","Bosnia and Herzegovina" : "BA","Botswana" : "BW","Brazil" : "BR","Brunei Darussalam" : "BN","Bulgaria" : "BG","Burkina Faso" : "BF","Burundi" : "BI","Cabo Verde" : "CV","Cambodia" : "KH","Cameroon" : "CM","Canada" : "CA","Central African Republic" : "CF","Chad" : "TD","Chile" : "CL","China" : "CN","Colombia" : "CO","Comoros" : "KM","Congo" : "CG","Costa Rica" : "CR","Côte d'Ivoire" : "CI","Croatia" : "HR","Cuba" : "CU","Cyprus" : "CY","Czechia" : "CZ","Democratic People's Republic of Korea" : "KP","Democratic Republic of the Congo" : "CD","Denmark" : "DK","Djibouti" : "DJ","Dominica" : "DM","Dominican Republic" : "DO","Ecuador" : "EC","Egypt" : "EG","El Salvador" : "SV","Equatorial Guinea" : "GQ","Eritrea" : "ER","Estonia" : "EE","Eswatini" : "SZ","Ethiopia" : "ET","Fiji" : "FJ","Finland" : "FI","France" : "FR","Gabon" : "GA","Gambia" : "GM","Georgia" : "GE","Germany" : "DE","Ghana" : "GH","Greece" : "GR","Grenada" : "GD","Guatemala" : "GT","Guinea" : "GN","Guinea-Bissau" : "GW","Guyana" : "GY","Haiti" : "HT","Honduras" : "HN","Hungary" : "HU","Iceland" : "IS","India" : "IN","Indonesia" : "ID","Iran (Islamic Republic of)" : "IR","Iraq" : "IQ","Ireland" : "IE","Israel" : "IL","Italy" : "IT","Jamaica" : "JM","Japan" : "JP","Jordan" : "JO","Kazakhstan" : "KZ","Kenya" : "KE","Kiribati" : "KI","Kuwait" : "KW","Kyrgyzstan" : "KG","Lao People's Democratic Republic" : "LA","Latvia" : "LV","Lebanon" : "LB","Lesotho" : "LS","Liberia" : "LR","Libya" : "LY","Liechtenstein" : "LI","Lithuania" : "LT","Luxembourg" : "LU","Madagascar" : "MG","Malawi" : "MW","Malaysia" : "MY","Maldives" : "MV","Mali" : "ML","Malta" : "MT","Marshall Islands" : "MH","Mauritania" : "MR","Mauritius" : "MU","Mexico" : "MX","Micronesia (Federated States of)" : "FM","Monaco" : "MC","Mongolia" : "MN","Montenegro" : "ME","Morocco" : "MA","Mozambique" : "MZ","Myanmar" : "MM","Namibia" : "NA","Nauru" : "NR","Nepal" : "NP","Netherlands" : "NL","New Zealand" : "NZ","Nicaragua" : "NI","Niger" : "NE","Nigeria" : "NG","North Macedonia" : "MK","Norway" : "NO","Oman" : "OM","Pakistan" : "PK","Palau" : "PW","Panama" : "PA","Papua New Guinea" : "PG","Paraguay" : "PY","Peru" : "PE","Philippines" : "PH","Poland" : "PL","Portugal" : "PT","Qatar" : "QA","Republic of Korea" : "KR","Republic of Moldova" : "MD","Romania" : "RO","Russian Federation" : "RU","Rwanda" : "RW","Saint Kitts and Nevis" : "KN","Saint Lucia" : "LC","Saint Vincent and the Grenadines" : "VC","Samoa" : "WS","San Marino" : "SM","Sao Tome and Principe" : "ST","Saudi Arabia" : "SA","Senegal" : "SN","Serbia" : "RS","Seychelles" : "SC","Sierra Leone" : "SL","Singapore" : "SG","Slovakia" : "SK","Slovenia" : "SI","Solomon Islands" : "SB","Somalia" : "SO","South Africa" : "ZA","South Sudan" : "SS","Spain" : "ES","Sri Lanka" : "LK","Sudan" : "SD","Suriname" : "SR","Sweden" : "SE","Switzerland" : "CH","Syrian Arab Republic" : "SY","Tajikistan" : "TJ","Thailand" : "TH","Timor-Leste" : "TL","Togo" : "TG","Tonga" : "TO","Trinidad and Tobago" : "TT","Tunisia" : "TN","Türkiye" : "TR","Turkmenistan" : "TM","Tuvalu" : "TV","Uganda" : "UG","Ukraine" : "UA","United Arab Emirates" : "AE","United Kingdom" : "GB","United Republic of Tanzania" : "TZ","United States of America" : "US","Uruguay" : "UY","Uzbekistan" : "UZ","Vanuatu" : "VU","Venezuela (Bolivarian Republic of)" : "VE","Viet Nam" : "VN","Yemen" : "YE","Zambia" : "ZM","Zimbabwe" : "ZW"
}

COUNTRY_CHOICES = tuple(sorted(((code, name) for name, code in countries.items()), key=lambda kv: kv[1]))

categories = {  'FIC': 'Fiction',    'LIT': 'Literary Fiction',    'HISF': 'Historical Fiction',    'SFF': 'Science Fiction',    'FAN': 'Fantasy',    'MYS': 'Mystery & Detective',    'THR': 'Thriller',    'ROM': 'Romance',    'HOR': 'Horror',    'SS': 'Short Stories',    'GN': 'Comics & Graphic Novels',    'YA': 'Young Adult',    'CH': 'Childrens' ,    'POE': 'Poetry',    'DRA': 'Drama & Plays',    'BIO': 'Biography',    'MEM': 'Memoir',    'HIS': 'History',    'TC': 'True Crime',    'ESS': 'Essays',    'SCI': 'Science',    'TECH': 'Technology',    'ENG': 'Engineering',    'MATH': 'Mathematics',    'PSY': 'Psychology',    'SOC': 'Social Sciences',    'PHI': 'Philosophy',    'REL': 'Religion & Spirituality',    'BUS': 'Business',    'ECO': 'Economics',    'FIN': 'Finance & Investing',    'LAW': 'Law',    'POL': 'Politics',    'HEA': 'Health & Fitness',    'EDU': 'Education',    'LAN': 'Language & Linguistics',    'ART': 'Art & Design',    'PHO': 'Photography',    'MUS': 'Music',    'TRV': 'Travel',    'COO': 'Cooking & Food',    'CRA': 'Crafts & DIY',    'NAT': 'Nature & Environment',    'REF': 'Reference',    'TB': 'Textbook',    'OTH': 'Other'
}

CATEGORY_CHOICES = tuple(categories.items())

sexs = { 'M' :'male' , 'F' :'female'}

SEX_CHOICES = tuple(sexs.items())


User = get_user_model()

# class User(models.Model):
#     id = models.CharField(blank=False,null=False)
#     phonenumber = models.CharField(blank=True,null=True)
#     firstname = models.CharField(max_length=50 , null=True, blank=False)
#     lastname = models.CharField(max_length=100 , null=True, blank=False)
#     email = models.CharField(max_length=150 , null=True, blank=False)
#     is_admin = models.BooleanField(null=False,blank=False)
#     update_at = jmodels.jDateField(null=True,blank=True)
#     created_at = jmodels.jDateField(null=True,blank=True)

#     def age(self):
#         if self.birth_date:
#             now = jmodels.jdatetime.date.today().year
#             return now - self.birth_date.year
#         return None

#     @property
#     def is_birthday(self):
#         if self.birth_date:
#             today = jmodels.jdatetime.date.today()
#             return (today.month == self.birth_date.month) and (today.day == self.birth_date.day)
    

class user_extra(models.Model):
    user_id = models.OneToOneField(to=User,on_delete=models.CASCADE, related_name="users_extra")
    sex = models.CharField(choices=SEX_CHOICES , null=True , blank=True)
    nationalcode = models.CharField(max_length=10 ,null=True , blank=True)
    update_at = jmodels.jDateField(auto_now_add=True,null=True,blank=True)
    created_at = jmodels.jDateField(auto_now=True,null=True,blank=True)


class Author(models.Model):
    name = models.CharField(max_length=150)
    bio = models.TextField(blank=True)
    birth_date = jmodels.jDateField(null=True,blank=True)
    country = models.CharField(max_length=2 , choices=COUNTRY_CHOICES , blank=True , null=True)
    sex = models.CharField(max_length=1 , choices=SEX_CHOICES , null=True , blank=True)


    @property
    def age(self):
        if self.birth_date:
            now = jmodels.jdatetime.date.today().year
            return now - self.birth_date.year
        return None

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Author_detail", kwargs={"pk": self.pk})



class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="author_books")
    category = models.CharField(max_length=4 , choices=CATEGORY_CHOICES,null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    published_date = jmodels.jDateField(null=True,blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self): return f"{self.title} — {self.author.name} - {self.category}"


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorites")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="favorited_by")
    date = jmodels.jDateField(auto_now_add=True,null=True,blank=True)

    class Meta:
        unique_together = ("user", "book")

