from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import authentication_classes, permission_classes
from audit_trail.views import *
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import date,datetime
# Create your views here.
#profile Crud
@swagger_auto_schema(
    method='post',
    operation_summary="Create a new Profile",
    request_body=ProfileSerializer,
    responses={201: ProfileSerializer}
)
@api_view(['GET', 'POST'])
def ProfileLists(request,id):
    if request.method == 'GET':
        profile = Profile.objects.filter(sacco_id=id)
        serializer = ProfileSerializer(profile, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            profile=serializer.save()
            create_audit_post_message(request,serializer,profile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    

@api_view(['GET', 'POST'])
def GlobalProfileLists(request):
    if request.method == 'GET':
        profile = Profile.objects.all()
        serializer = ProfileSerializer(profile, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            profile=serializer.save()
            create_audit_post_message(request,serializer,profile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      
@swagger_auto_schema(
    method='put',
    operation_summary="update a  Profile",
    request_body=ProfileSerializer,
    responses={201: ProfileSerializer}
)
@api_view(['GET', 'PUT', 'DELETE'])
def ProfileDetails(request, pk):
    try:
        profile = Profile.objects.get(pk=pk)
    except Profile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            create_audit_edit_message(request,serializer,profile)
            serializer.save()            
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        create_audit_delete_message(request,profile)
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
# UserModel Crud
@swagger_auto_schema(
    method='post',
    operation_summary="Create a new User",
    request_body=UsersModelSerializer,
    responses={201: UsersModelSerializer}
)
@api_view(['GET', 'POST'])
def UsersList(request,id):
    if request.method == 'GET':
        user = UsersModel.objects.filter(sacco_id=id)
        serializer = UsersModelSerializer(user, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = UsersModelSerializer(data=request.data)
        
        if UsersModel.objects.filter(**request.data).exists():
            raise serializers.ValidationError('This data already exists')
        if serializer.is_valid():
            try:
                user = UsersModel.objects.get(email=serializer.validated_data['email'])
                return Response({'Success': False, 'Code': 400, 'message': 'User already exists', 'user': user.id}, status=status.HTTP_400_BAD_REQUEST)
            except UsersModel.DoesNotExist:
                serializer.save()
                email = serializer.data['email']
                #password = get_random_string(10).lower()
                password = 'Test@123'
                user_model_instance = User.objects.create_user(username=email, password=password, email=email)
                
                #message = f'Welcome to Vlapp your login credentials are <br> url: app.emmerce.io <br> email: {email} <br> password: {password} '
                #subject = "Account Creation"
                #send_email(email, message, subject, client)
            
            
            
                create_audit_post_message(request,serializer,user_model_instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@swagger_auto_schema(
    method='put',
    operation_summary="update a  User",
    request_body=UsersModelSerializer,
    responses={201: UsersModelSerializer}
)
@api_view(['GET', 'PUT', 'DELETE'])
def UserDetails(request, pk):
    try:
        user = UsersModel.objects.get(pk=pk)
    except UsersModel.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UsersModelSerializer(user)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UsersModelSerializer(user, data=request.data)
        if serializer.is_valid():
            create_audit_edit_message(request,serializer,user)
            serializer.save()
            
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        create_audit_delete_message(request,user)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@swagger_auto_schema(
    method='post',
    operation_summary="Login",
    request_body=LoginSerilizer,
    responses={201: LoginSerilizer}
) 
@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def login_view(request):
    serializer = LoginSerilizer(data=request.data)
    if serializer.is_valid():
        Email = serializer.data['email']
        Password = serializer.data['password'] 

        try:            
            user = authenticate(request, username=Email, password=Password)
            if user is not None:
                if Email == 'superadmin@kingsway.co.ke':
                    refresh = RefreshToken.for_user(user)
                    action="LOGIN"
                    description=f"{Email} logged in successfully"
                    origin="Login"
                    ip_address=request.META.get('REMOTE_ADDR')
                    user_agent=request.META.get('HTTP_USER_AGENT')
                    x_forwarded_for=request.META.get('HTTP_X_FORWARDED_FOR')
                    add_system_logs(user, action, description, origin,ip_address,user_agent,x_forwarded_for)
                    return Response({'Success': 'True', 'Code': 200,
                                    'Details': {
                                        'user_type':'superadmin',
                                        'user': user.id,
                                        'refresh': str(refresh),
                                        'access': str(refresh.access_token),
                                    }}, status=status.HTTP_200_OK)
                login_user = UsersModel.objects.get(email=Email)
                #otp = get_random_string(6, allowed_chars='1234567890')
                otp = '123456'
                login_user.otp = otp
                login_user.save()
                return Response({'Success': 'True', 'Code': 200,
                                    'Details': "OTP sent","user":user.id,"email":Email}, status=status.HTTP_200_OK)
            else:
                action="LOGIN"
                description=f"{Email} failed to login"
                origin="Login"
                ip_address=request.META.get('REMOTE_ADDR')
                user_agent=request.META.get('HTTP_USER_AGENT')
                x_forwarded_for=request.META.get('HTTP_X_FORWARDED_FOR')
                add_system_logs(user, action, description, origin,ip_address,user_agent,x_forwarded_for)
                return Response({'Success': 'False', 'Code': 400,
                                    'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
                
        except ObjectDoesNotExist:
            action="LOGIN"
            description=f"{Email} failed to login"
            origin="Login"
            ip_address=request.META.get('REMOTE_ADDR')
            user_agent=request.META.get('HTTP_USER_AGENT')
            x_forwarded_for=request.META.get('HTTP_X_FORWARDED_FOR')
            add_system_logs(user, action, description, origin,ip_address,user_agent,x_forwarded_for)
            return Response({'Success': 'False', 'Code': 400,'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def verify_otp(request):
    email = request.data['email']
    otp = request.data['otp']
    user_id = request.data['user']
    try:
        user_main = UsersModel.objects.get(email=email,otp=otp) 
        user = User.objects.get(id=user_id)
        
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token
        
        action="LOGIN"
        description=f"{email} OTP Verification successfully"
        origin="Login"
        ip_address=request.META.get('REMOTE_ADDR')
        user_agent=request.META.get('HTTP_USER_AGENT')
        x_forwarded_for=request.META.get('HTTP_X_FORWARDED_FOR')
        add_system_logs(user, action, description, origin,ip_address,user_agent,x_forwarded_for)
               
        return Response({'Success': 'True',
                        'Code': 200,
                        'Details': {
                            'user': user_main.id,
                            'sacco': user_main.sacco_id,
                            'profile': user_main.profile_id,
                            'email': user_main.email,
                            'first_name': user_main.first_name,
                            'last_name': user_main.last_name,
                            'first_login': user_main.first_login,
                            'status': user_main.status,
                            'last_password_reset': user_main.last_password_reset,
                            'refresh': str(refresh),
                            'access': str(access_token),
                        }}, status=status.HTTP_200_OK)
                       
        
    except ObjectDoesNotExist:
        action="LOGIN"
        description=f"{email} OTP Verification Failed"
        origin="Login"
        ip_address=request.META.get('REMOTE_ADDR')
        user_agent=request.META.get('HTTP_USER_AGENT')
        x_forwarded_for=request.META.get('HTTP_X_FORWARDED_FOR')
        add_system_logs(user, action, description, origin,ip_address,user_agent,x_forwarded_for)
        return Response({'Success': 'False', 'Code': 400,
                            'message': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def reset_password(request):
    email = request.data['email']
    new_password = request.data['new_password']
    old_password = request.data['old_password']
    try:
        user_main = UsersModel.objects.get(email=email) 
        user = authenticate(request, username=email, password=old_password)
        if user:
            user_main.set_password(new_password)
            user_main.save()
            user_main.last_password_reset = datetime.now()
            user_main.first_login = False
            user_main.save()
            action="LOGIN"
            description=f"{email} Password Reset successfully"
            origin="Login"
            ip_address=request.META.get('REMOTE_ADDR')
            user_agent=request.META.get('HTTP_USER_AGENT')
            x_forwarded_for=request.META.get('HTTP_X_FORWARDED_FOR')
            add_system_logs(user, action, description, origin,ip_address,user_agent,x_forwarded_for)
            return Response({'Success': 'True',
                            'Code': 200,
                            'Details': {
                                'user': user_main.id,
                                'sacco': user_main.sacco_id,
                                'profile': user_main.profile_id,
                                'email': user_main.email,
                                'first_name': user_main.first_name,
                                'last_name': user_main.last_name,
                                'first_login': user_main.first_login,
                                'status': user_main.status,
                                'last_password_reset': user_main.last_password_reset,
                            }}, status=status.HTTP_200_OK)
            
        else:
            action="LOGIN"
            description=f"{email} Password Reset Failed"
            origin="Login"
            ip_address=request.META.get('REMOTE_ADDR')
            user_agent=request.META.get('HTTP_USER_AGENT')
            x_forwarded_for=request.META.get('HTTP_X_FORWARDED_FOR')
            add_system_logs(user, action, description, origin,ip_address,user_agent,x_forwarded_for)
            return Response({'Success': 'False', 'Code': 400,
                            'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        
        
    except ObjectDoesNotExist:
        action="LOGIN"
        description=f"{email} Password Reset Failed"
        origin="Login"
        ip_address=request.META.get('REMOTE_ADDR')
        user_agent=request.META.get('HTTP_USER_AGENT')
        x_forwarded_for=request.META.get('HTTP_X_FORWARDED_FOR')
        add_system_logs(user, action, description, origin,ip_address,user_agent,x_forwarded_for)
        return Response({'Success': 'False', 'Code': 400,
                            'message': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['POST'])
def forgot_password(request):
    email = request.data['email']
    created_at = request.data['created_at']
    try:
        user_main = UsersModel.objects.get(email=email) 
        password = get_random_string(10).lower()
        try:
            user = User.objects.get(username=email)
            user.set_password(password)
            user.save()
            
            user_main.first_login=True
            user_main.save()
            
            action="LOGIN"
            description=f"{email} Forgot Password successfully"
            origin="Login"
            ip_address=request.META.get('REMOTE_ADDR')
            user_agent=request.META.get('HTTP_USER_AGENT')
            x_forwarded_for=request.META.get('HTTP_X_FORWARDED_FOR')
            add_system_logs(user, action, description, origin,ip_address,user_agent,x_forwarded_for)
        except ObjectDoesNotExist:
            return Response({'Success': 'False', 'Code': 400,
                            'message': 'User Doesnt exist'}, status=status.HTTP_400_BAD_REQUEST)
        
        
    except ObjectDoesNotExist:       
        return Response({'Success': 'False', 'Code': 400,
                            'message': 'User Doesnt exist'}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(["GET"])
def actions_get_view(request, id):
    try:        
        actions = Actions.objects.filter(parent_id=None)
        sacco_id=None
        actions_tree = []
        children_tree = []
        TempPermissions.objects.filter(profile_id=id,sacco_id=sacco_id).delete()
        TempSubPermissions.objects.filter(profile_id=id,sacco_id=sacco_id).delete()
        for action in actions:
            submodules = Actions.objects.filter(parent=action.id)
            for submodule in submodules:
                try:
                    permission = NewPermissions.objects.get(
                        profile_id=id, action_id=submodule.id
                    )
                    create = permission.create
                    read = permission.read
                    update = permission.update
                    delete = permission.delete


                except:
                    create = False
                    read = False
                    update = False
                    delete = False

                    
                
                n = TempPermissions.objects.create(
                    create=create,
                    read=read,
                    update=update,
                    delete=delete,
                    name=submodule.name,
                    parent=action.id,
                    profile_id=id,
                    action_id=submodule.id,
                    sacco_id=sacco_id,
                )
                print("id=" + str(n.pk))
                subsubmodules = Actions.objects.filter(parent=submodule.id)
                for subsubmodule in subsubmodules:
                    try:
                        permission = NewPermissions.objects.get(
                            profile_id=id, action_id=subsubmodule.id
                        )
                        create = permission.create
                        read = permission.read
                        update = permission.update
                        delete = permission.delete

                    except:
                        create = False
                        read = False
                        update = False
                        delete = False

                    p = TempSubPermissions.objects.create(
                        create=create,
                        db_table_name=subsubmodule.table_name,
                        is_custom_field=subsubmodule.custom_field,
                        read=read,
                        update=update,
                        delete=delete,
                        name=subsubmodule.name,
                        bachildren_id=n.id,
                        parent=submodule.id,
                        profile_id=id,
                        action_id=subsubmodule.id,
                        sacco_id=sacco_id,
                    )

                    fouthmodules = Actions.objects.filter(parent=subsubmodule.id)
                    for fouthmodule in fouthmodules:
                        try:
                            permission = NewPermissions.objects.get(
                                profile_id=id, action_id=fouthmodule.id
                            )
                            create = permission.create
                            read = permission.read
                            update = permission.update
                            delete = permission.delete

                        except:
                            create = False
                            read = False
                            update = False
                            delete = False

                        TempFourthPermissions.objects.create(
                            create=create,
                            db_table_name=fouthmodule.table_name,
                            is_custom_field=fouthmodule.custom_field,
                            read=read,
                            update=update,
                            delete=delete,
                            name=fouthmodule.name,
                            childrens_id=p.id,
                            parents=subsubmodule.id,
                            profile_id=id,
                            action_id=fouthmodule.id,
                            sacco_id=sacco_id,
                        )
            try:
                permission = NewPermissions.objects.get(
                    profile_id=id, action_id=action.id
                )
                create = permission.create
                read = permission.read
                update = permission.update
                delete = permission.delete

                print(permission)
                
            except:
                create = False
                read = False
                update = False
                delete = False

            perms = TempPermissions.objects.filter(
                profile_id=id,parent=action.id,sacco_id=sacco_id
            )

            serializer1 = TempPermissionsserializer(perms, many=True)

            # print(serializer1)

            actions_tree.append(
                {
                    "action": action.id,
                    "name": action.name,
                    "create": create,
                    "read": read,
                    "update": update,
                    "delete": delete,
                    "children": serializer1.data,
                }
            )
        return Response({"permissions": actions_tree}, status=200)
    except ObjectDoesNotExist:
        return Response({"success": "false"}, status=400)
    


@api_view(["GET"])
def sacco_actions_get_view(request, id):
    try:  
        client_profile=id      
        sacco_id=Profile.objects.get(id=id).sacco_id
        permissions = NewPermissions.objects.filter(profile_id=client_profile,read=True)
        action_ids = permissions.values_list('action_id', flat=True)
        actions = Actions.objects.filter(parent_id=None,id__in=action_ids)
        
        actions_tree = []
        children_tree = []
        TempPermissions.objects.filter(profile_id=id,sacco_id=sacco_id).delete()
        TempSubPermissions.objects.filter(profile_id=id,sacco_id=sacco_id).delete()
        for action in actions:
            submodules = Actions.objects.filter(parent=action.id)
            for submodule in submodules:
                try:
                    permission = NewPermissions.objects.get(
                        profile_id=id, action_id=submodule.id
                    )
                    create = permission.create
                    read = permission.read
                    update = permission.update
                    delete = permission.delete


                except:
                    create = False
                    read = False
                    update = False
                    delete = False

                    
                
                n = TempPermissions.objects.create(
                    create=create,
                    read=read,
                    update=update,
                    delete=delete,
                    name=submodule.name,
                    parent=action.id,
                    profile_id=id,
                    action_id=submodule.id,
                    sacco_id=sacco_id,
                )
                print("id=" + str(n.pk))
                subsubmodules = Actions.objects.filter(parent=submodule.id)
                for subsubmodule in subsubmodules:
                    try:
                        permission = NewPermissions.objects.get(
                            profile_id=id, action_id=subsubmodule.id
                        )
                        create = permission.create
                        read = permission.read
                        update = permission.update
                        delete = permission.delete

                    except:
                        create = False
                        read = False
                        update = False
                        delete = False

                    p = TempSubPermissions.objects.create(
                        create=create,
                        db_table_name=subsubmodule.table_name,
                        is_custom_field=subsubmodule.custom_field,
                        read=read,
                        update=update,
                        delete=delete,
                        name=subsubmodule.name,
                        bachildren_id=n.id,
                        parent=submodule.id,
                        profile_id=id,
                        action_id=subsubmodule.id,
                        sacco_id=sacco_id,
                    )

                    fouthmodules = Actions.objects.filter(parent=subsubmodule.id)
                    for fouthmodule in fouthmodules:
                        try:
                            permission = NewPermissions.objects.get(
                                profile_id=id, action_id=fouthmodule.id
                            )
                            create = permission.create
                            read = permission.read
                            update = permission.update
                            delete = permission.delete

                        except:
                            create = False
                            read = False
                            update = False
                            delete = False

                        TempFourthPermissions.objects.create(
                            create=create,
                            db_table_name=fouthmodule.table_name,
                            is_custom_field=fouthmodule.custom_field,
                            read=read,
                            update=update,
                            delete=delete,
                            name=fouthmodule.name,
                            childrens_id=p.id,
                            parents=subsubmodule.id,
                            profile_id=id,
                            action_id=fouthmodule.id,
                            sacco_id=sacco_id,
                        )
            try:
                permission = NewPermissions.objects.get(
                    profile_id=id, action_id=action.id
                )
                create = permission.create
                read = permission.read
                update = permission.update
                delete = permission.delete

                print(permission)
                
            except:
                create = False
                read = False
                update = False
                delete = False

            perms = TempPermissions.objects.filter(
                profile_id=id,parent=action.id,sacco_id=sacco_id
            )

            serializer1 = TempPermissionsserializer(perms, many=True)

            # print(serializer1)

            actions_tree.append(
                {
                    "action": action.id,
                    "name": action.name,
                    "create": create,
                    "read": read,
                    "update": update,
                    "delete": delete,
                    "children": serializer1.data,
                    "client":sacco_id,
                    "action_ids":action_ids,
                    "client_profile":client_profile


                }
            )
        return Response({"permissions": actions_tree}, status=200)
    except ObjectDoesNotExist:
        return Response({"success": "false"}, status=400)
    
    
    

@api_view(["POST"])
def permissions_add_view(request):
    serializer = Permissionsserializer(data=request.data)
    if serializer.is_valid():
        company = serializer.data.get("sacco")
        profile = serializer.data.get("profile")
        action = serializer.data.get("action")
        create = serializer.data.get("create")
        read = serializer.data.get("read")
        update = serializer.data.get("update")
        delete = serializer.data.get("delete")
        status = serializer.data.get("status")
        print(action)
        # validating for already existing data
        try:
            id = NewPermissions.objects.get(
                profile_id=profile, action_id=action, sacco_id=company
            ).id
            serializer = NewPermissions.objects.get(pk=id)
            data = Permissionsserializer(instance=serializer, data=request.data)
            if data.is_valid():
                data.save()
                modules = f"parameters"
                activity = f"Added new permission"

                return Response(
                    {"Success": "True", "Code": 200, "message": "Successfully Updated"},
                    status=200,
                )
            else:
                return Response(data=serializer.errors, status=400)
        except ObjectDoesNotExist:
            print("noma")
            if NewPermissions.objects.filter(**request.data).exists():
                raise serializers.ValidationError("This data already exists")
            NewPermissions.objects.create(
                sacco_id=company,
                profile_id=profile,
                action_id=action,
                create=create,
                read=read,
                update=update,
                delete=delete,
                status=status,
            )

            return Response(
                {"Success": "True", "Code": 201, "message": "Successfully Added"},
                status=201,
            )

    return Response(serializer.errors, status=400)


@api_view(["GET"])
def permissions_get_view(request,id):
    permissions = Sacco.objects.get(id=id).profile_id
    profiles = Profile.objects.filter(Q(sacco_id=id) | Q(id=permissions))
    serializer = ProfileSerializer(profiles, many=True)
    return Response({'Success': 'True', 'Code': 200, 'message': 'Successful' ,'data': serializer.data,}, status=status.HTTP_200_OK)
# # permissions
    