# Generated by Django 4.0.1 on 2023-01-06 14:19

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('taggit', '0004_alter_taggeditem_content_type_alter_taggeditem_tag'),
    ]

    operations = [
        migrations.CreateModel(
            name='Registrations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('is_student', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='ColCourse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_name', models.CharField(blank=True, max_length=200, null=True, unique=True, verbose_name='Course')),
                ('slug', models.SlugField(blank=True, max_length=250, null=True)),
            ],
            options={
                'db_table': 'col_course',
            },
        ),
        migrations.CreateModel(
            name='ColDept',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department_name', models.CharField(blank=True, max_length=200, null=True, unique=True, verbose_name='Department')),
                ('department_abbreviation', models.CharField(blank=True, max_length=200, null=True)),
                ('slug', models.SlugField(blank=True, max_length=250, null=True)),
            ],
            options={
                'db_table': 'col_dept',
            },
        ),
        migrations.CreateModel(
            name='thesisDB',
            fields=[
                ('thesis_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, max_length=200, null=True, unique=True)),
                ('adviser', models.CharField(blank=True, max_length=200, null=True)),
                ('published_date', models.DateField(blank=True, null=True)),
                ('published_year', models.IntegerField(choices=[(1968, 1968), (1969, 1969), (1970, 1970), (1971, 1971), (1972, 1972), (1973, 1973), (1974, 1974), (1975, 1975), (1976, 1976), (1977, 1977), (1978, 1978), (1979, 1979), (1980, 1980), (1981, 1981), (1982, 1982), (1983, 1983), (1984, 1984), (1985, 1985), (1986, 1986), (1987, 1987), (1988, 1988), (1989, 1989), (1990, 1990), (1991, 1991), (1992, 1992), (1993, 1993), (1994, 1994), (1995, 1995), (1996, 1996), (1997, 1997), (1998, 1998), (1999, 1999), (2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020), (2021, 2021), (2022, 2022), (2023, 2023)], default=2023)),
                ('published_month', models.CharField(choices=[('January', 'January'), ('February', 'February'), ('March', 'March'), ('April', 'April'), ('May', 'May'), ('June', 'June'), ('July', 'July'), ('August', 'August'), ('September', 'September'), ('October', 'October'), ('November', 'November'), ('December', 'December')], default='January', max_length=15)),
                ('pdf', models.FileField(blank=True, null=True, upload_to='pdf/', validators=[django.core.validators.FileExtensionValidator(['pdf'])])),
                ('date_created', models.DateField(auto_now_add=True, null=True)),
                ('published_status', models.CharField(choices=[('Approved', 'Approve'), ('Rejected', 'Reject')], default='Pending', max_length=10)),
                ('abstract', models.TextField(blank=True, null=True)),
                ('reason', models.TextField(blank=True, null=True)),
                ('slug', models.SlugField(blank=True, max_length=250, null=True)),
                ('apa', models.CharField(blank=True, max_length=300, null=True)),
                ('mla', models.CharField(blank=True, max_length=300, null=True)),
                ('chicago', models.CharField(blank=True, max_length=300, null=True)),
                ('submission_agreement', models.BooleanField(default=False)),
                ('course', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='libraryApp.colcourse', verbose_name='Course')),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
                ('uploaded_by', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'thesis_storage',
            },
        ),
        migrations.CreateModel(
            name='RequestPDF',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_evaluated', models.DateTimeField(blank=True, null=True)),
                ('request_status', models.CharField(choices=[('Approved', 'Approve'), ('Declined', 'Decline')], default='Pending', max_length=10)),
                ('reason', models.TextField(blank=True, null=True)),
                ('slug', models.SlugField(blank=True, max_length=250, null=True)),
                ('thesis', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='libraryApp.thesisdb')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='colcourse',
            name='coldep_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='libraryApp.coldept'),
        ),
        migrations.CreateModel(
            name='Authors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=200, null=True)),
                ('last_name', models.CharField(blank=True, max_length=200, null=True)),
                ('thesis', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='thesis', to='libraryApp.thesisdb')),
            ],
        ),
    ]
