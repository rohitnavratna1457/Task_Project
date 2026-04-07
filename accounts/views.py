# accounts/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from .models import User, Calculation
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    CalculationInputSerializer
)
from .services import IllustrationService


# ✅ PAGINATION (5 per page)
class CustomPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 20


# ✅ REGISTER API (GET + POST)
class RegisterAPIView(APIView):

    def get(self, request):
        users = User.objects.all().order_by('-id')

        paginator = CustomPagination()
        paginated_qs = paginator.paginate_queryset(users, request)

        serializer = RegisterSerializer(paginated_qs, many=True)

        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "User registered successfully"
            }, status=201)

        return Response(serializer.errors, status=400)


# ✅ LOGIN API
class LoginAPIView(APIView):

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            user = User.objects.filter(email=email, password=password).first()

            if user:
                return Response({
                    "message": "Login successful",
                    "user_id": user.id
                }, status=200)

            return Response({
                "error": "Invalid credentials"
            }, status=401)

        return Response(serializer.errors, status=400)


# ✅ CALCULATION API (FULL LOGIC)
class CalculateAPIView(APIView):

    # 🔹 GET (with pagination)
    def get(self, request):

        calculations = Calculation.objects.all().order_by('-created_at')

        paginator = CustomPagination()
        paginated_qs = paginator.paginate_queryset(calculations, request)

        data = []

        for calc in paginated_qs:
            data.append({
                "id": calc.id,
                "input": calc.input_data,
                "output": calc.output_data,
                "created_at": calc.created_at
            })

        return paginator.get_paginated_response(data)

    # 🔹 POST (CORE ENGINE)
    def post(self, request):

        serializer = CalculationInputSerializer(data=request.data)

        if serializer.is_valid():
            try:
                validated_data = serializer.validated_data

                # ✅ STEP 1: Run business logic (keep date object)
                result = IllustrationService().execute(validated_data)

                # ✅ STEP 2: Convert dob → string for JSON storage
                input_data = {
                    **validated_data,
                    "dob": str(validated_data["dob"])
                }

                # ✅ STEP 3: Save to DB
                user = User.objects.first()

                calc = Calculation.objects.create(
                    user=user,
                    input_data=input_data,
                    output_data=result
                )

                # ✅ STEP 4: Return structured response
                return Response({
                    "message": "Calculation successful",
                    "data": {
                        "id": calc.id,
                        "input": input_data,
                        "output": result
                    }
                }, status=200)

            except Exception as e:
                return Response({
                    "error": str(e)
                }, status=400)

        return Response(serializer.errors, status=400)


# ✅ HISTORY API (PAGINATION)
class HistoryAPIView(APIView):

    def get(self, request):

        calculations = Calculation.objects.all().order_by('-created_at')

        paginator = CustomPagination()
        paginated_qs = paginator.paginate_queryset(calculations, request)

        data = []

        for calc in paginated_qs:
            data.append({
                "id": calc.id,
                "input": calc.input_data,
                "output": calc.output_data,
                "created_at": calc.created_at
            })

        return paginator.get_paginated_response(data)