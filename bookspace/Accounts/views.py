from django.http import JsonResponse
from supabase import create_client
from django.conf import settings
import json
from django.views.decorators.csrf import csrf_exempt

# Initialize Supabase client
supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)



@csrf_exempt
def signup(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data.get("email")
        password = data.get("password")
        try:
            supabase.auth.sign_up({"email": email, "password": password})
            return JsonResponse({"status": "success", "message": "User created"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    return JsonResponse({"status": "error", "message": "Only POST allowed"})

@csrf_exempt
def login(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data.get("email")
        password = data.get("password")
        try:
            user = supabase.auth.sign_in_with_password({"email": email, "password": password})
            if user.user:
                return JsonResponse({"status": "success", "user": user.user.email})
            else:
                return JsonResponse({"status": "error", "message": "Invalid credentials"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    return JsonResponse({"status": "error", "message": "Only POST allowed"})
