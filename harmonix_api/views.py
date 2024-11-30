# from django.shortcuts import render
# from harmonix_api.models import User
# from django.http import JsonResponse
# # Create your views here.
# def user_list(request):
#     Users = User.objects.all()
#     data = {
#         'users': list(Users.values())
#     }

#     return JsonResponse(data)

# def user_details(request, pk):
#     user = User.objects.get(pk=pk)
    
#     data = {
#         'fullname': user.fullname,
#         'email': user.email,
#         'username': user.username,
#         'password': user.password,
#     }
    
#     return JsonResponse(data)