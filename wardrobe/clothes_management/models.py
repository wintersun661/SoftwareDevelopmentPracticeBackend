from django.db import models
from mongoengine import *
from authentication.models import User

class Cloth(DynamicDocument):
    id_ = IntField()
    owner = ReferenceField(User, required=True)
    usage_count = IntField(default=0)
    brand = StringField(max_length=50)
    category = StringField(max_length=50)
    size = StringField(max_length=50)
    

class ClothesManager:
    
    #TODO: distributed incremental id
    id_ = -1
    
    @classmethod
    def get_incremental_id(cls):
        cls.id_ += 1
        return cls.id_
    
    @classmethod
    def cloth2json(cls, cloth):
        return {
            'id_': cloth.id_,
            'owner': cloth.owner.username,
            'usage_count': cloth.usage_count,
            'brand': cloth.brand,
            'category': cloth.category,
            'size': cloth.size,
        }
    
    @classmethod
    def save_clothes(cls, clothes, username):
        if not isinstance(clothes, list):
            response = {
                'status': '104',
                'message': 'Invalid clothes',
            }
        else:
            #1. save the clothes in MongoDB
            #2. count how many clothes are successfully saved
            #3. respond with the information of successfully saved data
            owner = User.get_user(username)
            saved_clothes = []
            unsaved_clothes = []
            for cloth in clothes:
                #the user is only allowed to save his/her own clothes
                if cloth.get('owner') == username:
                    cloth_ = Cloth(owner = owner)
                    #TODO: extract and save more information
                    if 'usage_count' in cloth:
                        cloth_.usage_count = cloth['usage_count']
                    if 'brand' in cloth:
                        cloth_.brand = cloth['brand']
                    if 'category' in cloth:
                        cloth_.category = cloth['category']
                    if 'size' in cloth:
                        cloth_.size = cloth['size']
                    if 'color' in cloth:
                        cloth_.color = cloth['color']
                    cloth_.id_ = ClothesManager.get_incremental_id()
                    cloth_.save()
                    saved_clothes.append(ClothesManager.cloth2json(cloth_))
                else:
                    unsaved_clothes.append(cloth)
            response = {
                'status': '000',
                'message': 'Saved sucessfully',
                'data':{
                    'num': len(saved_clothes),
                    'saved_clothes': saved_clothes,
                    'unsaved_clothes': unsaved_clothes,
                }
            }
        return response
    
    @classmethod
    def get_clothes(cls, filters):
        #Pattern: filters
        print(filters['owner'])
        filters['owner'] = User.get_user(filters['owner'])
        #TODO: Range as a query option.
        clothes = Cloth.objects.filter(**filters)
        print(clothes)
        clothes = [] if clothes == None else [ClothesManager.cloth2json(cloth) for cloth in clothes]
        response = {
            'status': '000',
            'message': 'Query made successfully',
            'data':{
                'num': len(clothes),
                'clothes': clothes,
            }
        }
        return response