from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Contributor, Submission, PastPaper



class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = '__all__'

    def validate_email(self, value):
        return value.lower()

    def validate_file(self, value):

            if not value.name.lower().endswith('.pdf'):
                raise serializers.ValidationError("Only PDF files are accepted.")

            max_file_size = 30 * 10**6

            if value.size > max_file_size:
                raise serializers.ValidationError("File size should be less than 30MB.")
            
            return value
            


class ContributorSerializer(serializers.ModelSerializer):


    # name = serializers.CharField(
    #     validators=[
    #         UniqueValidator(queryset=Contributor.objects.all())
    #     ]
    # )

    class Meta:
        model = Contributor
        fields = '__all__'

        extra_kwargs = {
            'linkedIn': {
                'required': True
            }
        }


    def validate_email(self, value):
        modified_value = value.lower()
        contributor_exists = Contributor.objects.filter(email=modified_value).exists()

        if contributor_exists:
            raise serializers.ValidationError("This email is already in use.")

        return modified_value
    


class PastPaperSerializer(serializers.ModelSerializer):

    # submission_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = PastPaper
        fields = '__all__'

        extra_kwargs = {
            # 'submission_id': {
            #     'required': True,
            # },
            'submitted_by': {
                'required': True
            }
        }

        def validate_file(self, value):

            if not value.name.lower().endswith('.pdf'):
                raise serializers.ValidationError("File must be in PDF format.")

            max_file_size = 30 * 10**6

            if value.size > max_file_size:
                raise serializers.ValidationError("File size must be upto than 30MB.")
            
            return value


    # def validate_submitted_by(self, value):
    #     contributor = Contributor.objects.get(name__iexact=value)
    #     return contributor.id