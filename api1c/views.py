from rest_framework.response import Response
from rest_framework.views import APIView

from landing.models import Product
from .serializers import ProductCreateSerializer
from cart.cart import Cart


class ProductCreateView(APIView):
    def post(self, request):
        # cart = Cart(request)
        # cart.clear()
        # Product.objects.filter(store=request.data['store']).delete()

        product = ProductCreateSerializer(data=request.data)
        if product.is_valid():
            product.save()
            return Response(status=201)
        else:
            return Response(status=400)

# {
# "id_code" : "paracetomol",
# "store" : 3,
# "name":"tabletka",
# "price":17800,
# "quantity":10
# }
