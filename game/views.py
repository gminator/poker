from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from game.models import Classifier
from game.exceptions import * 
from rest_framework import status

# Create your views here.
class ClassifierView(APIView):
	#authentication_classes = [authentication.TokenAuthentication]
	#permission_classes = [permissions.IsAdminUser]

	def post(self, request, format=None):
		"""
		Return a list of all users.
		"""
		try:
			classifier = Classifier()
			classifier.parse(request.data["cards"])

			return Response({
				"hand" : classifier.evaluate(),
				"cards" : classifier.to_json()
			})
		except GameException as e:
			return Response({ "error" : str(e) }, status.HTTP_400_BAD_REQUEST)
		except: 
			return Response({ "error" : "System Error"},  status.HTTP_500_INTERNAL_SERVER_ERROR)