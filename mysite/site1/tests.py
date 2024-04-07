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


# luu y instance dai dien cho du lieu da co trong db
# validated_data du lieu duoc gui vao 
    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.title = validated_data.get('title', instance.title)
        instance.save()
        
        # xu ly logic cho phương thuc submodel1 
        if 'submodel1' in validated_data:
            submodel1_data_list = validated_data.get('submodel1', [])
            bien = False
            for submodel1_data in submodel1_data_list:
                temp = submodel1_data["name"]
                for submodel1 in instance.submodel1.all():
                    if temp == submodel1.name:
                        bien = True
                        submodel1.age = submodel1_data["age"]
                        submodel1.save()
                        break
            if bien:
                print("Da update submodel1")
            else:
                print("Khong tim thay")
        
        if 'submodel2' in validated_data:
            submodel2_data_list = validated_data.get('submodel2', [])
            bien = False
            for submodel2_data in submodel2_data_list:
                temp = submodel2_data["name"]
                for submodel2 in instance.submodel2.all():
                    if temp == submodel2.name:
                        bien = True
                        submodel2.address = submodel2_data["address"]
                        submodel2.description = submodel2_data["description"]
                        submodel2.save()
                        break
            if bien:
                print("Da update submodel2")
            else:
                print("Khong tim thay")
    
    
    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.title = validated_data.get('title', instance.title)
        instance.save()
        
        # Xử lý logic cho phương thức submodel1 
        if 'submodel1' in validated_data:
            submodel1_data_list = validated_data.get('submodel1', [])
            for submodel1_data in submodel1_data_list:
                SubModel1.objects.update_or_create(
                    name=submodel1_data["name"], 
                    defaults={'age': submodel1_data["age"]}
                )
            print("Đã cập nhật hoặc thêm mới SubModel1 dựa trên name.")
            
        # Tương tự cho SubModel2
        if 'submodel2' in validated_data:
            submodel2_data_list = validated_data.get('submodel2', [])
            for submodel2_data in submodel2_data_list:
                SubModel2.objects.update_or_create(
                    name=submodel2_data["name"],
                    defaults={
                        'address': submodel2_data["address"],
                        'description': submodel2_data["description"]
                    }
                )
            print("Đã cập nhật hoặc thêm mới SubModel2 dựa trên name.")

        return instance
    


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
            
        if 'submodel1' in validated_data:
            submodel1_data_list = validated_data.get('submodel1', [])
            for submodel1_data in submodel1_data_list:
                name = submodel1_data.pop('name', None)
                if name is not None:
                    submodel1, _ = SubModel1.objects.update_or_create(name=name, defaults=submodel1_data)
                else:
                    print("Tên không được cung cấp cho  SubModel1.")
        # Tương tự cho SubModel2
        if 'submodel2' in validated_data:
            submodel2_data_list = validated_data.get('submodel2', [])
            for submodel2_data in submodel2_data_list:
                SubModel2.objects.update_or_create(
                    name=submodel2_data["name"],
                    defaults={
                        'address': submodel2_data["address"],
                        'description': submodel2_data["description"]
                    }
                )
            print("Đã cập nhật hoặc thêm mới SubModel2 dựa trên name.")

        return instance

    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.title = validated_data.get('title', instance.title)
        instance.save()
        
        if 'submodel1' in validated_data:
            submodel1_data_list = validated_data.get('submodel1', [])
            for submodel1_data in submodel1_data_list:
                name = submodel1_data.pop('name', None)
                if name is not None:
                    submodel1, _ = SubModel1.objects.update_or_create(name=name, defaults=submodel1_data)
                else:
                    print("Tên không được cung cấp cho  SubModel1.")
        # Tương tự cho SubModel2
        if 'submodel2' in validated_data:
            submodel2_data_list = validated_data.get('submodel2', [])
            for submodel2_data in submodel2_data_list:
                SubModel2.objects.update_or_create(
                    name=submodel2_data["name"],
                    defaults={
                        'address': submodel2_data["address"],
                        'description': submodel2_data["description"]
                    }
                )
            print("Đã cập nhật hoặc thêm mới SubModel2 dựa trên name.")
        return instance
    
    

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