from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.http import require_GET
from core.models import Users, Products  # ✅ import Products model

@require_GET
def login(request):
    phone = request.GET.get("phone")
    password = request.GET.get("password")

    if not phone or not password:
        return JsonResponse({"error": "Phone and password required"}, status=400)

    try:
        user = Users.objects.get(phone=phone, password=password)
        # ✅ Redirect to dashboard if login succeeds
        # return redirect("http://localhost:5174/dashboard")
        # Or return JSON if you want frontend control:
        return JsonResponse({
            "message": "Login successful",
            "user": {
                "id": user.userid,
                "fullname": user.fullname,
                "phone": user.phone,
                "role": user.role
            }
        })
    except Users.DoesNotExist:
        return JsonResponse({"error": "Invalid phone or password"}, status=401)


@require_GET
def get_user(request, user_id):
    try:
        user = Users.objects.get(userid=user_id)

          # Fetch products linked to this user (artisan/vendor)
        products = Products.objects.filter(artisanid=user.userid).values(
            "productid",
            "name",
            "description",
            "price",
            "stock",
            "categoryid",
            "createdat",
            "updatedat"
        )
        return JsonResponse({
            "id": user.userid,
            "name": user.fullname,
            "phone": user.phone,
            "type": user.role,  # match frontend expected key
            "email": user.email,
            "products": list(products)  # include related products
         }, safe=False)
    except Users.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)


@require_GET
def get_products(request):
    user_id = request.GET.get("userId")

    if not user_id:
        return JsonResponse({"error": "userId is required"}, status=400)

  # ✅ Use ArtisanID instead of vendor_id
    products = Products.objects.filter(artisanid_id=user_id).values(
        "productid", "name", "price", "description", "stock", "categoryid", "createdat", "updatedat"
    )

    return JsonResponse(list(products), safe=False)
