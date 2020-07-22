from rest_framework import serializers

from landing.models import Product


class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        # exclude = ('category', 'description', 'image',)
        fields = ('id_code', 'store', 'name', 'price', 'quantity')

    def create(self, validated_data):
        id_code = validated_data.get("id_code", None)
        store = validated_data.get("store", None)
        name = validated_data.get("name", None)
        price = validated_data.get("price", None)
        quantity = validated_data.get("quantity", None)
        # print(Product.objects.get(id_code=id_code, store=store), 1)
        if Product.objects.filter(id_code=id_code, store=store).first():
            product = Product.objects.update(
                id_code=validated_data.get("id_code", None),
                store=validated_data.get("store", None),
                name=validated_data.get("name", None),
                price=validated_data.get("price", None),
                quantity=validated_data.get("quantity", None),
            )
        else:
            product = Product.objects.create(
                id_code=validated_data.get("id_code", None),
                store=validated_data.get("store", None),
                name=validated_data.get("name", None),
                price=validated_data.get("price", None),
                quantity=validated_data.get("quantity", None),
            )


        # product = Product.objects.update_or_create(
        #     id_code=validated_data.get("id_code", None),
        #     store=validated_data.get("store", None),
        #     name=validated_data.get("name", None),
        #     price=validated_data.get("price", None),
        #     quantity=validated_data.get("quantity", None),
        #     defaults={
        #         'price': validated_data.get("price", None),
        #         'quantity': validated_data.get("quantity"),
        #     }
        #
        # )
        return product
