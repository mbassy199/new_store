from django.shortcuts import render
from userauths.models import User
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from store.models import Product, Category, Cart, Tax
from store.serializers import ProductSerializer, CategorySerializer, CartSerializer
from decimal import Decimal

class CategoryListView(generics.ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = (AllowAny,)


class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.filter(status="published")
    permission_classes = (AllowAny,)


class ProductDetailView(generics.RetrieveAPIView):
    serializer_class = ProductSerializer

    def get_object(self):
        slug = self.kwargs.get('slug')
        return Product.objects.get(slug=slug)


class CartAPI(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        payload = request.data

        # Debugging: Log the payload
        print(f"Received payload: {payload}")

        # Required fields
        required_fields = ['product_id', 'user_id', 'price', 'shipping_amount', 'country', 'cart_id']
        errors = {}

        # Validate fields
        for field in required_fields:
            if not payload.get(field):
                errors[field] = "This field is required."

        # If there are missing fields, return a 400 response
        if errors:
            return Response(
                {"error": "Validation error", "details": errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Extract and validate values
            product_id = int(payload['product_id'])
            user_id = int(payload['user_id'])
            qty = int(payload.get('qty', 1))
            price = Decimal(payload['price'])
            shipping_amount = Decimal(payload['shipping_amount'])
            country = payload['country']
            cart_id = payload['cart_id']
            color = payload.get('color', '')
            size = payload.get('size', '')

            # Retrieve the product and user
            product = Product.objects.get(id=product_id)
            user = User.objects.get(id=user_id) if user_id != "undefined" else None

            # Compute additional values
            tax = Tax.objects.filter(country=country).first()
            tax_rate = tax.rate / 100 if tax else 0
            sub_total = price * qty
            shipping_amount = shipping_amount * qty
            tax_fee = tax_rate * sub_total
            service_fee = 0.1 * sub_total
            total = sub_total + shipping_amount + service_fee + tax_fee

            # Check for an existing cart
            cart = Cart.objects.filter(cart_id=cart_id, product=product).first()

            if cart:
                # Update the existing cart
                cart.qty = qty
                cart.sub_total = sub_total
                cart.shipping_amount = shipping_amount
                cart.tax_fee = tax_fee
                cart.color = color
                cart.size = size
                cart.country = country
                cart.cart_id = cart_id
                cart.service_fee = service_fee
                cart.total = total
                cart.save()
                return Response({"message": "Cart updated successfully."}, status=status.HTTP_200_OK)
            else:
                # Create a new cart
                Cart.objects.create(
                    product=product,
                    user=user,
                    qty=qty,
                    sub_total=sub_total,
                    shipping_amount=shipping_amount,
                    tax_fee=tax_fee,
                    color=color,
                    size=size,
                    country=country,
                    cart_id=cart_id,
                    service_fee=service_fee,
                    total=total
                )
                return Response({"message": "Cart created successfully."}, status=status.HTTP_201_CREATED)

        except Product.DoesNotExist:
            return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        except (ValueError, Decimal.InvalidOperation):
            return Response({"error": "Invalid input data."}, status=status.HTTP_400_BAD_REQUEST)
