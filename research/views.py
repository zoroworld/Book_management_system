# apps/research/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ResearchPaper
from .serializers import ResearchPaperSerializer
from django.shortcuts import get_object_or_404

# List all research papers or create a new one
class ResearchPaperListAPI(APIView):
    def get(self, request):
        papers = ResearchPaper.objects.all()
        serializer = ResearchPaperSerializer(papers, many=True)
        return Response(
            {"message": "Fetching the research papers.", "data": serializer.data},
            status=status.HTTP_200_OK
        )

    def post(self, request):
        serializer = ResearchPaperSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Research paper created.", "data": serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Retrieve, update, or delete a specific research paper
class ResearchPaperDetailAPI(APIView):
    def get_object(self, pk):
        return get_object_or_404(ResearchPaper, pk=pk)

    def get(self, request, pk):
        paper = self.get_object(pk)
        serializer = ResearchPaperSerializer(paper)
        return Response(
            {"message": "Research paper fetched.", "data": serializer.data},
            status=status.HTTP_200_OK
        )

    def put(self, request, pk):
        paper = self.get_object(pk)
        serializer = ResearchPaperSerializer(paper, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Research paper updated.", "data": serializer.data},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        paper = self.get_object(pk)
        paper.delete()
        return Response(
            {"message": f"Research paper with ID {pk} has been deleted."},
            status=status.HTTP_204_NO_CONTENT
        )
