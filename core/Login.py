from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.http import require_GET
from core.models import Users

@require_GET
def login(request):
    phone = request.GET.get("phone")
    password = request.GET.get("password")

    if not phone or not password:
        return JsonResponse({"error": "Phone and password required"}, status=400)

    try:
        user = Users.objects.get(phone=phone, password=password)
        # ✅ Redirect to dashboard if login succeeds
        return redirect("http://localhost:5174/dashboard")
        # Or return JSON if you want frontend control:
        # return JsonResponse({
        #     "message": "Login successful",
        #     "user": {
        #         "id": user.userid,
        #         "fullname": user.fullname,
        #         "phone": user.phone,
        #         "role": user.role
        #     }
        # })
    except Users.DoesNotExist:
        return JsonResponse({"error": "Invalid phone or password"}, status=401)
