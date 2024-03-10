from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from Backend.models import Job, CandidatesApplied
from Backend.serializers import JobSerializer, CandidatesAppliedSerializer
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count, Avg, Min, Max
from .filters import JobFilter

from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404







# Create your views here

@csrf_exempt
def JobAPI(request,ID=0):
    if request.method=="GET":
        filterset=JobFilter(request.GET,queryset=Job.objects.all().order_by('id'))
        serializer=JobSerializer(filterset.qs,many=True)


        return JsonResponse(serializer.data,safe=False)
    elif request.method=="POST":
        x=JSONParser().parse(request)
        y=JobSerializer(data=x)
        if y.is_valid():
            y.save()
            return JsonResponse("Data saved succesfully...!",safe=False)
        return JsonResponse("invalid data...!",safe=False)
@api_view(['PUT'])
def updateJob(request, pk):
        job = get_object_or_404(Job, id=pk)

        job.title = request.data['title']
        job.description = request.data['description']
        job.email = request.data['email']
        job.address = request.data['address']
        job.jobType = request.data['jobType']
        job.education = request.data['education']
        job.industry = request.data['industry']
        job.experience = request.data['experience']
        job.salary = request.data['salary']
        job.positions = request.data['positions']
        job.company = request.data['company']

        job.save()

        serializer = JobSerializer(job, many=False)

        return Response(serializer.data)


@csrf_exempt
def JobIDAPI(request,pk):
    if request.method == "GET":
        y = Job.objects.get(id=pk)
        obj = JobSerializer(y)

    # Return the serialized data as a JSON response
        return JsonResponse(obj.data, safe=False)
    elif request.method == "PUT":
        x = JSONParser().parse(request)
        y = Job.objects.get(id=pk)
        obj = JobSerializer(y, data=x)
        if obj.is_valid():
            obj.save()
            return JsonResponse("Data updated succesfully.....", safe=False)
        return JsonResponse("Failed to update......!", safe=False)
    elif request.method == "DELETE":

        y = Job.objects.get(id=pk)
        y.delete()
        return JsonResponse("Data Deleted..!", safe=False)


def TopicStatsAPI(request, topic):
    if request.method == "GET":
        jobs = Job.objects.filter(title__icontains=topic)

        if not jobs.exists():
            return JsonResponse({'message': f'No stats found for {topic}'}, safe=False)

        stats = jobs.aggregate(
            total_jobs=Count('title'),
            avg_positions=Avg('positions'),
            avg_salary=Avg('salary'),
            min_salary=Min('salary'),
            max_salary=Max('salary')
        )

        return JsonResponse(stats, safe=False)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def applyToJob(request, pk):

    user = request.user
    job = get_object_or_404(Job, id=pk)

    if user.userprofile.resume == '':
        return Response({ 'error': 'Please upload your resume first' }, status=status.HTTP_400_BAD_REQUEST)

    if job.lastDate < timezone.now():
        return Response({ 'error': 'You can not apply to this job. Date is over' }, status=status.HTTP_400_BAD_REQUEST)

    alreadyApplied = job.candidatesapplied_set.filter(user=user).exists()

    if alreadyApplied:
        return Response({ 'error': 'You have already apply to this job.' }, status=status.HTTP_400_BAD_REQUEST)


    jobApplied = CandidatesApplied.objects.create(
        job = job,
        user = user,
        resume = user.userprofile.resume
    )

    return Response({
        'applied': True,
        'job_id': jobApplied.id
    },
    status=status.HTTP_200_OK
    )



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getCurrentUserAppliedJobs(request):

    args = { 'user_id': request.user.id }

    jobs = CandidatesApplied.objects.filter(**args)

    serializer = CandidatesAppliedSerializer(jobs, many=True)

    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def isApplied(request, pk):

    user = request.user
    job = get_object_or_404(Job, id=pk)

    applied = job.candidatesapplied_set.filter(user=user).exists()

    return Response(applied)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getCurrentUserJobs(request):

    args = { 'user': request.user.id }

    jobs = Job.objects.filter(**args)
    serializer = JobSerializer(jobs, many=True)

    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getCandidatesApplied(request, pk):
    user = request.user
    job = get_object_or_404(Job, id=pk)

    # Check if the requesting user is the owner of the job

    # Fetch candidates if the user has the necessary permissions
    candidates = job.candidatesapplied_set.all()
    candidates_count = job.candidatesapplied_set.count()

    # Serialize the candidates data
    serializer = CandidatesAppliedSerializer(candidates, many=True)

    # Return a dictionary containing both the serialized data and the candidates_count
    return Response({'candidates': serializer.data, 'candidates_count': candidates_count})
