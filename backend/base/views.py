import requests
import json
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse, HttpResponse

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination


from .models import Contributor, PastPaper, Submission
from .serializers import ContributorSerializer, SubmissionSerializer, PastPaperSerializer


from .helpers.utils import createContributor, deleteSubmission

# Create your views here.


class ContributorPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50


class SubmissionView(APIView):


    def get(self, request):
        submissions = Submission.objects.all()

        serializer = SubmissionSerializer(submissions, many=True)
        return Response(serializer.data)



    def post(self, request):
        
        serializer = SubmissionSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class SubmissionDetailView(APIView):


    def delete(self, request, pk):


        response = deleteSubmission(pk)

        return Response(response[0], status=response[1])



class ContributorView(APIView):

    pagination_class = ContributorPagination

    def get(self, request):
        contributors = Contributor.objects.all()


        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(contributors, request)


        serializer = ContributorSerializer(paginated_queryset, many=True)
        
        response_data = {
            'count': paginator.page.paginator.count,
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
            'results': serializer.data
        }

        return Response(response_data, status=status.HTTP_200_OK)


    def post(self, request):

        response = createContributor(data=request.data)
        serializer = ContributorSerializer(data=request.data)

        return Response(response[0], status=response[1])



class PaperPaperView(APIView):


    def post(self, request):




        # try:
        #     submission = Submission.objects.get(id=request.data.get('submitted_by', None))
        
        # except Submission.DoesNotExist:
        #     return Response({
        #         'submiited_by': [
        #             "Not provided or not valid"
        #         ]
        #     }, status=status.HTTP_400_BAD_REQUEST)
    

        # try:
        #     contributor = Contributor.objects.get(email=submission.email)

        # except Contributor.DoesNotExist:

        #     url = request.build_absolute_uri(reverse('contributors'))
        #     # Retrieve the relative URL using the name and prepend the scheme
        #     response = createContributor(url, submission)
            
        #     if response.status_code == 400:

        #         return Response(response, status=status.HTTP_400_BAD_REQUEST)
            
        
        # contributor = Contributor.objects.get(email=submission.email)
        # print(contributor.id)
        
        # request.data._mutable = True
        # request.data['submitted_by'] = contributor.id
        try:
            submission = Submission.objects.get(id=request.data.get('submission_id', ''))
        except Submission.DoesNotExist:
            return Response({
                'message': "submission_id is not given or is not valid"
            }, status=status.HTTP_400_BAD_REQUEST)

        
        try:
            contributor = Contributor.objects.get(email=submission.email)

        except Contributor.DoesNotExist:

            response = createContributor(data={
                'name': submission.name,
                'email': submission.email,
                'linkedIn': submission.linkedIn
            })

            if response[1] == status.HTTP_400_BAD_REQUEST:
                return Response(response[0], status=response[1])
            
        # think of a better approch
        request.POST._mutable = True
        request.data['submitted_by'] = Contributor.objects.get(email=submission.email).id
        request.data['file'] = submission.file
        
        serializer = PastPaperSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            response = deleteSubmission(submission_id=submission.id)

            if response[1] == status.HTTP_400_BAD_REQUEST:
                return Response(response[0], status=response[1])

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


    def get(self, request):
        pastpapers = PastPaper.objects.all()

        serializer = PastPaperSerializer(pastpapers, many=True)
        return Response(serializer.data)
