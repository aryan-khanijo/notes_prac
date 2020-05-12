from django.db import models

# Create your models here.


class Semester(models.Model):

    Semester = models.CharField(
        max_length = 20
    )

    class Meta:
        verbose_name_plural = 'Semester'

class Subjects(models.Model):
    # Year List
    Years = (
        ('First','1st'),
        ('Second','2nd'),
        ('Third','3rd')
    )

    # end List

    subject = models.CharField(
        max_length = 40
    )
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)

    Year = models.CharField(
        choices = Years,
        max_length = 15,
        default = 'Third'
    )

    class Meta:
        verbose_name_plural = 'Subjects'


class Notes(models.Model):
    # Field Required
    # Username from login
    # Semester from User (input list)
    # Subject from user (input list)
    # Source from User (input list)
    # Topic from user (input field)
    # File from User (input upload)
    # approval
    
    # Lists required

    Units = (
        ('1','One'),
        ('2','Two'),
        ('3','Three'),
        ('4','Four'),
        ('0','Complete Syllabus')
    )

    sources = (
        ("0","Self/Friend's"),
        ("1","Teacher's")
    )

    # End list

    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE)
        
    unit = models.CharField(
        choices = Units,
        max_length = 1
    )

    Topic = models.CharField(
        max_length = 50
    )

    source = models.CharField(
        choices = sources,
        max_length = 1
    )

    uploaded_by = models.CharField(
        max_length = 50
    )

    pdf = models.FileField(
        upload_to = 'notes/Notes/'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Notes'