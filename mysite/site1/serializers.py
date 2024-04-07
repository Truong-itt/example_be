from rest_framework import serializers
from .models import MainModel, SubModel1, SubModel2
from rest_framework.exceptions import NotFound

class SubModel1Serializer(serializers.ModelSerializer):
    class Meta:
        model = SubModel1
        fields = '__all__'

class SubModel2Serializer(serializers.ModelSerializer):
    class Meta:
        model = SubModel2
        fields = '__all__'

class MainModelSerializer(serializers.ModelSerializer):
    submodel1 = SubModel1Serializer(many=True, required=False)
    submodel2 = SubModel2Serializer(many=True, required=False)

    class Meta:
        model = MainModel
        fields = ['id','title', 'submodel1', 'submodel2']

    def create(self, validated_data):
        
        submodel1_data_list = validated_data.pop('submodel1')
        submodel2_data_list = validated_data.pop('submodel2')
        
        mainmodel = MainModel.objects.create(**validated_data)

        for submodel1_data in submodel1_data_list:
            submodel1, created = SubModel1.objects.get_or_create(**submodel1_data)
            mainmodel.submodel1.add(submodel1)

        for submodel2_data in submodel2_data_list:
            submodel2, created = SubModel2.objects.get_or_create(**submodel2_data)
            mainmodel.submodel2.add(submodel2)
        
        return mainmodel
    
    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.title = validated_data.get('title', instance.title)
        instance.save()
        
        # Xử lý logic cho phương thức submodel1 
        # if 'submodel1' in validated_data:
        #     submodel1_data_list = validated_data.get('submodel1', [])
        #     for submodel1_data in submodel1_data_list:
        #         submodel1_id = submodel1_data.pop('id', None)
        #         if submodel1_id is not None:
        #             submodel1, _ = SubModel1.objects.update_or_create(id=submodel1_id, defaults=submodel1_data)
            
        # if 'submodel1' in validated_data:
        #     submodel1_data_list = validated_data.get('submodel1', [])
        #     for submodel1_data in submodel1_data_list:
        #         name = submodel1_data.pop('name', None)
        #         print
        #         if name is not None:
        #             submodel1, _ = SubModel1.objects.update_or_create(name=name, defaults=submodel1_data)
        #         else:
        #             print("Tên không được cung cấp cho  SubModel1.")
        if 'submodel1' in validated_data:
            submodel1_data_list = validated_data.pop('submodel1', [])
            existing_names = [submodel1.name for submodel1 in instance.submodel1.all()]
            for submodel1_data in submodel1_data_list:
                name = submodel1_data.get('name')
                if name in existing_names:
                    # Nếu tên đã tồn tại, cập nhật đối tượng hiện có
                    submodel1 = SubModel1.objects.filter(name=name).first()
                    for key, value in submodel1_data.items():
                        setattr(submodel1, key, value)
                    submodel1.save()
                else:
                    # Nếu tên không tồn tại, tạo mới và liên kết với instance chính
                    submodel1 = SubModel1.objects.create(**submodel1_data)
                    instance.submodel1.add(submodel1)

        # Tương tự cho SubModel2
        if 'submodel2' in validated_data:
            submodel2_data_list = validated_data.get('submodel2', [])
            existing_names = [submodel2.name for submodel2 in instance.submodel2.all()]
            for submodel2_data in submodel2_data_list:
                name = submodel2_data.get('name')
                if name in existing_names:
                    # Nếu tên đã tồn tại, cập nhật đối tượng hiện có
                    submodel2 = SubModel2.objects.filter(name=name).first()
                    for key, value in submodel2_data.items():
                        setattr(submodel2, key, value)
                    submodel2.save()
                else:
                    # Nếu tên không tồn tại, tạo mới và liên kết với instance chính
                    submodel2 = SubModel2.objects.create(**submodel2_data)
                    instance.submodel2.add(submodel2)


        return instance

class MainModelSerializer_Delete(serializers.ModelSerializer):
    submodel1 = SubModel1Serializer(many=True, required=False)
    submodel2 = SubModel2Serializer(many=True, required=False)
    submodel1_removal_requests = serializers.ListField(child=serializers.CharField(), write_only=True, required=False)

    class Meta:
        model = MainModel
        fields = ['id', 'title', 'submodel1', 'submodel2', 'submodel1_removal_requests']

    def update(self, instance, validated_data):
        # Xử lý yêu cầu xoá
        removal_requests = validated_data.pop('submodel1_removal_requests', [])
        for name_to_remove in removal_requests:
            try:
                submodel1_instance = instance.submodel1.get(name=name_to_remove)
                submodel1_instance.delete()
            except SubModel1.DoesNotExist:
                # Bạn có thể log lỗi hoặc xử lý khác tùy ý
                pass

        # Tiếp tục cập nhật instance như bình thường nếu cần
        # ...
        return super().update(instance, validated_data)

'''

class MainModelSerializer_Delete(serializers.ModelSerializer):
    submodel1 = SubModel1Serializer(many=True, required=False)
    submodel2 = SubModel2Serializer(many=True, required=False)

    class Meta:
        model = MainModel
        fields = ['id','title', 'submodel1', 'submodel2','submodel1_removal_requests']
    def update(self, instance, validated_data):
        # Xử lý yêu cầu xoá
        removal_requests = validated_data.pop('submodel1_removal_requests', [])
        print(f"removal_requests: {removal_requests}")
        for name_to_remove in removal_requests:
            print(f"name_to_remove: {name_to_remove}")
            try:
                submodel1_instance = instance.submodel1.get(name=name_to_remove)
                submodel1_instance.delete()
                print(f"Removed SubModel1 with name: {name_to_remove}")
            except SubModel1.DoesNotExist:
                print(f"SubModel1 with name {name_to_remove} does not exist.")

        return instance
'''
    


'''
    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.title = validated_data.get('title', instance.title)
        instance.save()

        # Xử lý cho SubModel1
        if 'submodel1' in validated_data:
            print("SubModel1 trước khi clear:")
            for submodel1 in instance.submodel1.all():
                print(f"ID: {submodel1.id}, Age: {submodel1.age}, Name: {submodel1.name}") 
            submodel1_data_list = validated_data.get('submodel1', [])
            instance.submodel1.clear()
            for submodel1_data in submodel1_data_list:
                print(f"SubModel1 data: {submodel1_data}")
                submodel1, created = SubModel1.objects.get_or_create(**submodel1_data)
                instance.submodel1.add(submodel1)

        # Xử lý cho SubModel2 tương tự như SubModel1
        if 'submodel2' in validated_data:
            # print("SubModel2 trước khi clear:", instance.submodel2.all())
            print("SubModel2 trước khi clear:")
            for submodel2 in instance.submodel2.all():
                print(f"ID: {submodel2.id}, Detail: {submodel2.address}, Description: {submodel2.description}, Name: {submodel2.name}")
            print("SubModel2 sau khi clear:")
            # print du lieu ra 
            submodel2_data_list = validated_data.get('submodel2', [])
            
            instance.submodel2.clear()
            for submodel2_data in submodel2_data_list:
                print(f"SubModel2 data: {submodel2_data}")
                print(submodel2_data.get('address', 'Không có địa chỉ'))
                print(submodel2_data["address"])
                submodel2, created = SubModel2.objects.get_or_create(**submodel2_data)
                instance.submodel2.add(submodel2)

        return instance

'''

    
'''

    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.title = validated_data.get('title', instance.title)
        instance.save()

        # Cập nhật SubModel1
        submodel1_data_list = validated_data.get('submodel1')
        if submodel1_data_list is not None:
            instance.submodel1.clear()
            for submodel1_data in submodel1_data_list:
                submodel1, created = SubModel1.objects.get_or_create(**submodel1_data)
                instance.submodel1.add(submodel1)

        # Kiểm tra xem 'submodel2' có trong validated_data không
        # Chỉ cập nhật SubModel2 nếu có dữ liệu mới được cung cấp
        if 'submodel2' in validated_data:
            submodel2_data_list = validated_data.get('submodel2')
            instance.submodel2.clear()
            for submodel2_data in submodel2_data_list:
                submodel2, created = SubModel2.objects.get_or_create(**submodel2_data)
                instance.submodel2.add(submodel2)
            
        return instance

'''
