from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .serializers import UserSerializer
from .models import Realtor,Renter
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.views import PasswordResetView
from django.utils.decorators import method_decorator
from rest_framework import viewsets
from .serializers import RealtorBankDetailsSerializer , RealtorBusinessDoucmentSerializer , PropertySerializer , MultiplePropertyImageUploadSerializer,\
TransactionsSerializer
from .helpermodule import getAuthUserId,send_realtor_account_creation_mail,send_renter_verification_mail ,flush_user_token
from property.models import Location , PropertyType , Property , PropertyImage 
from rest_framework.parsers import MultiPartParser, FormParser # to handle image uploads 
from payments.models import Payment
from django.db.models import Q

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from property.models import Property
from .serializers import PropertySerializer



@method_decorator(csrf_exempt, name='dispatch')
class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# @method_decorator(csrf_exempt, name='dispatch')
class CustomPasswordResetView(PasswordResetView):
    email_template_name = 'reset_password_email.html'  
custom_password_reset_view = csrf_exempt(CustomPasswordResetView.as_view())


@csrf_exempt
@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def user_login(request):
    # Get user credentials from the request data
    username = request.data.get('username')
    password = request.data.get('password')
    # Authenticate the user
    user = authenticate(username=username, password=password)
    if user is not None:
        resp ={'success': "true"}
        try:
            if Renter.objects.get(user = user)!= None :
                resp['first_name'] = user.first_name
                resp['last_name'] = user.last_name
                resp['is_active'] = "true" if user.is_active == 1 else "False"
        except:
            resp['business_name'] = "x"
            resp['business_verified'] = "False"
        # Generate or retrieve the authentication token for the user
        token, created = Token.objects.get_or_create(user=user)
        resp['token'] = token.key        # Return authentication token in the response
        login(request,user) #update last login 
        return Response(resp)
    else:
        return Response({'error': 'Invalid credentials'}, status=400)
    
@csrf_exempt
@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def user_logout(request):
    status = flush_user_token(request)
    if status:
        return Response({'success': 'True' ,'msg' : 'you have been successfully logged out '})
    return Response({'error': 'something went wrong , please try again '}, status=400)


#CRUD for Realtor bank details 
class RealtorBankDetailsViewSet(viewsets.ModelViewSet):
    queryset = Realtor.objects.all()
    serializer_class = RealtorBankDetailsSerializer
    # permission_classes = [IsAuthenticated]  # Require authentication for all operations

    def list(self, request):
        #handles getting banki details related to the users 
        # grab the auth id and fetch bank details for th customer 
        msg = getAuthUserId(request)
        if not msg['error'] :
            realtor = Realtor.objects.get(user=msg['id'])
            # print(realtor.Bank_details.value())
            serializer = RealtorBankDetailsSerializer(realtor)
            return Response(serializer.data)
        return Response({'error': msg['msg']} , status = 400)
    
    def create(self, request, *args, **kwargs):
        #handles adding and updating bank details 
        serializer = self.get_serializer(data=request.data)
        msg = getAuthUserId(request)
        if serializer.is_valid() and not msg['error'] :
                Realtor.objects.filter(user_id = msg['id']).update(Bank_details = serializer['Bank_details'])
                return Response({'success':"true"})
        return Response({'error':msg['msg']},status = 400)
    
    def destroy(self, request, *args, **kwargs):
        # handle deletion ,clearing of bank details 
        msg = getAuthUserId(request)
        if not msg['error'] :
            realtor = Realtor.objects.get(user=msg['id'])
            realtor.Bank_details = None
            realtor.save()
            return Response(status=204)
        return Response({'error':msg['msg']},status = 400)
    


    #CRUD for Realtor business document
class RealtorBusinessDocumentViewSet(viewsets.ModelViewSet):
    queryset = Realtor.objects.all()
    serializer_class = RealtorBusinessDoucmentSerializer
    # permission_classes = [IsAuthenticated]  # Require authentication for all operations

    def list(self, request):
        #handles getting banki details related to the users 
        # grab the auth id and fetch bank details for th customer 
        msg = getAuthUserId(request)
        if not msg['error'] :
            realtor = Realtor.objects.get(user=msg['id'])
            # print(realtor.Bank_details.value())
            serializer = RealtorBankDetailsSerializer(realtor)
            return Response(serializer.data)
        return Response({'error': msg['msg']} , status = 400)
    
    def create(self, request, *args, **kwargs):
        #handles adding and updating realtor business details 
        serializer = self.get_serializer(data=request.data)
        msg = getAuthUserId(request)
        if serializer.is_valid() and not msg['error'] :
                Realtor.objects.filter(user_id = msg['id']).update(Bank_details = serializer['Bank_details'])
                return Response({'success':"true"})
        return Response({'error':msg['msg']},status = 400)
    
    def destroy(self, request, *args, **kwargs):
        # handle deletion ,clearing of bank details 
        msg = getAuthUserId(request)
        if not msg['error'] :
            realtor = Realtor.objects.get(user=msg['id'])
            realtor.Bank_details = None
            realtor.save()
            return Response(status=204)
        return Response({'error':msg['msg']},status = 400)


#crud for realtor to create , list and update listing 
# authorized by admin on creation , update  and deletion only approved by admin 
class PropertyListingViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    parser_classes = (MultiPartParser, FormParser)
    
    # get the list of properties created and published by realtor 
    def list(self, request , pk):
        msg = getAuthUserId(request)
        if not msg['error'] :
            realtor_properties = Property.objects.filter(realtor__user__id = msg['id'])
            if realtor_properties is []:
                realtor_properties = Property.objects.get(pk = pk)

            serializer = self.serializer_class(realtor_properties ,  many=True , context={'request': request})
            return Response(serializer.data)
        return Response({'error': msg['msg']} , status = 400)
    
    def create(self, request, *args, **kwargs):
        #handles creating and updating the property listings  | add one property at a time 
        serializer = self.get_serializer(data=request.data)
        images = [request.data['image1'], request.data['image1'], request.data['image1']] 
        msg = getAuthUserId(request)
        if serializer.is_valid() and not msg['error'] :
                serializer.validated_data['realtor'] = Realtor.objects.get(user_id = msg['id'])
                instance = serializer.save()
                for img  in images:  # upload images after creating the instance of the property 
                    PropertyImage.objects.create(property_id = instance.id , upload = img)
                return Response({'success':"true"})
        return Response({'error':msg['msg']},status = 400)
    

  # let the viewset default update handle the the control when the method is called 
    
    def destroy(self, request,pk, *args, **kwargs):
        # handle deletion of  unpublished  of listings   * condition is , they should not be published
        msg = getAuthUserId(request)
        if not msg['error'] :
            realtor = Realtor.objects.get(user=msg['id'])
            Property.objects.filter(realtor = realtor  , pk = pk , is_published = 0).delete()
            return Response(status=204)
        return Response({'error':msg['msg']},status = 400)
    

class GetLocationPriceTypeNamesAndIds(viewsets.ModelViewSet):
    #window onload , set options  on front end  | unauthorized 
    # accepts a query parameter and passes key for location , price or type 
    def list(self, request  , *args, **kwargs):
        location = request.query_params.get('location')
        price = request.query_params.get('price')
        types= request.query_params.get('type')
        
        data = {}
        if location:
            queryset = Location.objects.all()
            for i in queryset :
                data[i.id ]= i.city
            return Response({'location': data})
        
        if types :
            # queryset = PropertyType.objects.all()
            # for i in queryset :
            #     data[i.id ]= i.type
            # return Response({'type': data })
            return Response( { 'type' :  {'1B': '1 Bedroom', '2B': '2 Bedroom','CA': 'Commercial Apartment','MT': 'Mortgage Apartment','4S': 'For Sale','4R': 'For Rent'}})
        
        if price  :
            return Response({"price" : {'1': "Below Ghs 5000  " , '2' : " Above GHS 5000 " }})
        
        return Response({'error': "no query id passed "})
        


#search sort , view  , paginate property listing for renter # todo
    # a serializer accepts text for search 
    # url accepts  query parameters for sorting and filtering 
    # authorized for rentor , pop up login 

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10  # Adjust the page size as needed
    page_size_query_param = 'page_size'
    max_page_size = 100

@api_view(['GET'])
def property_search_sort_filter(request):
    # Filtering based on URL query parameters
    type_filter = request.query_params.get('type')
    location_filter = request.query_params.get('location')
    price_min_filter = request.query_params.get('price_min')
    price_max_filter = request.query_params.get('price_max')
    search_query = request.query_params.get('search')

    properties = Property.objects.filter(is_published=True)

    if type_filter:
        properties = properties.filter(property_types__type=type_filter)
    
    if location_filter:
        properties = properties.filter(Location__city=location_filter.lower())
    
    if price_min_filter:
        properties = properties.filter(price__gte=price_min_filter)
    
    if price_max_filter:
        properties = properties.filter(price__lte=price_max_filter)

    # Search functionality using Q objects
    if search_query:
        properties = properties.filter(
            Q(name__icontains=search_query) | Q(description__icontains=search_query)
        )

    # Sorting based on URL query parameter 'ordering' (default to price ascending)
    ordering = request.query_params.get('ordering', 'price')
    properties = properties.order_by(ordering)

    # Apply pagination using CustomPageNumberPagination
    paginator = CustomPageNumberPagination()
    paginated_properties = paginator.paginate_queryset(properties, request)

    # Serialize the filtered, sorted, and paginated properties
    serializer = PropertySerializer(paginated_properties,  many=True , context={'request': request})

    # Build the response data including pagination information
    response_data = {
        'count': paginator.page.paginator.count,
        'next': paginator.get_next_link(),
        'previous': paginator.get_previous_link(),
        'results': serializer.data
    }

    return Response(response_data)


#for  renter #todo
class BuyOrViewDetailPropertyListingViewSet(viewsets.ModelViewSet):
    # buy / view detail accepts the product ID 
    # if buy , pop up paystack 
    # if view , return extra images and data for the the product 
    # authorized  by renter pop up login 
    pass



# remeber to paginate this  # both renter (t) and realtor (t and s ) 
class ViewSettlementTransactionDataViewSet(viewsets.ReadOnlyModelViewSet): # its a readonly 
     # view transactions for renter and realtor and view settlement for only realtor 
    # authorized  by renter/admin  pop up login 
    queryset = Payment.objects.all()
    serializer_class = TransactionsSerializer 

    def list(self , request , *args):
        msg = getAuthUserId(request)
        if not msg['error'] :
            data =  Payment.objects.filter(\
                Q(renter__user__id=msg['id']) | Q(property__realtor__user__id = msg['id'])
            )
            serializer = self.serializer_class(data , many=True )
            return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        # Restrict the update method
        return Response({"detail": "Update method is not allowed."}, status=400)

    def destroy(self, request, *args, **kwargs):
        # Restrict the delete method
        return Response({"detail": "Delete method is not allowed."}, status=400)




from django.shortcuts import render
def landing_page(request):
    return render(request, 'home.html')