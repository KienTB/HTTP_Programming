from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import json
from urllib.parse import parse_qs

def home(request):
    return render(request,'home.html')

def parse_form_urlencoded(data):
    # Phân tích cú pháp dữ liệu từ dạng application/x-www-form-urlencoded\
    data_str = data.decode('utf-8')

    parsed_data = parse_qs(data_str)

    # Chuyển đổi từ điển dữ liệu đã phân tích sang kiểu dữ liệu dict
    result = {key: value[0] for key, value in parsed_data.items()}

    return result

@csrf_exempt
def user_list(request):
    if request.method == 'GET':
        users = User.objects.all()
        data = [{'id': user.id, 'username': user.username, 'email': user.email} for user in users]
        return JsonResponse(data, safe=False)
 
    elif request.method == 'POST': 
        data = request.POST
        user = User.objects.create(username=data['username'], email=data['email'], password=data['password'])
        user.save()
        return JsonResponse({'message': 'User created successfully'}, status=201)

@csrf_exempt
def user_detail(request, user_id):
    #Nếu đối tượng với user_id đã được tìm thấy trong cơ sở dữ liệu, phương thức get_object_or_404 sẽ trả về đối tượng đó. Tuy nhiên, nếu không tìm thấy đối tượng với user_id, nó sẽ tạo ra một lỗi HTTP 404 ("Page not found") và hiển thị một trang lỗi 404 cho người dùng.
    user = get_object_or_404(User, pk=user_id) #pk = primary key

    if request.method == 'GET':
        data = {'id': user.id, 'username': user.username, 'email': user.email}
        return JsonResponse(data)

    elif request.method == 'PUT':
        data =parse_form_urlencoded(request.body)
        user.username = data['username']
        user.email = data['email']
        
        user.save()
        return JsonResponse({'message': 'User updated successfully'})
        
        
        # request_data là một từ điển Python chứa dữ liệu từ nội dung của yêu cầu PUT


    elif request.method == 'DELETE':
        user.delete()
        return JsonResponse({'message': 'User deleted successfully'})
    


