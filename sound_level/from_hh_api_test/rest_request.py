__author__ = 'mdu'
import pprint
import data_source_config


BASE_ADDRESS = 'base_address'
COMMON_HEADERS = 'common_headers'
HTTP_COMMAND = 'http_command'
REQUESTS = 'requests'
REQUEST_TYPE = 'request_type'
REQUEST_PATH = 'request_path'
REQUEST_HEADERS = 'request_headers'


class rest_request_:

    def create_request(self,ds_name,request_type, **param):
        cls=self.__class__
        self.request={}
        if param:
            self.request['request_url']=cls.get_request_url(cls,ds_name,request_type, **param)
        else:
            self.request['request_url']=cls.get_request_url(ds_name,request_type)
        self.request['request_headers']=cls.get_request_headers(ds_name,request_type)
        self.request['request_http_command']=cls.get_request_http_command(ds_name,request_type)
        for k in self.request:
            if self.request is None:
                return None
        return request
class rest_request:

    def create_request(self,ds_name,request_type, **param):
        cls=self.__class__
        request={}
        if param:
            request['request_url']=cls.get_request_url(cls,ds_name,request_type, **param)
        else:
            request['request_url']=cls.get_request_url(ds_name,request_type)
        request['request_headers']=cls.get_request_headers(ds_name,request_type)
        request['request_http_command']=cls.get_request_http_command(ds_name,request_type)
        for k in request:
            if request is None:
                return None
        return request


    #def get_request_url(ds_name,request_type, param = None):
    #@staticmethod
    @classmethod
    def get_request_url(cls,ds_name,request_type, **param):
        url = cls.get_object('.'.join([ds_name, BASE_ADDRESS]))+'/'
        url +=  cls.get_object('.'.join([ds_name,REQUESTS,request_type,REQUEST_PATH]))
        if param :
            return url.format(**param)
        return url

    @classmethod
    def get_request_http_command(cls,ds_name,request_type):
        command = cls.get_object('.'.join([ds_name,REQUESTS, request_type,HTTP_COMMAND]))
        return command

    @classmethod
    def get_request_headers(cls,ds_name,request_type):
        headers = cls.get_object('.'.join([ds_name, COMMON_HEADERS]))
        request_headers = cls.get_object('.'.join([ds_name,REQUESTS, request_type,REQUEST_HEADERS]))
        if request_headers is not None:
            headers.update(request_headers)
        return headers

    @classmethod
    def get_object(cls,object_path):
        object_name_list=object_path.split('.')
        obj = data_source_config.data_source
        for idx,object_name in enumerate(object_name_list):
            if not hasattr(obj,'get'):
                print("Error. Wrong type of intermediate object '%s' (target object path is '%s')" % (".".join(object_name_list[:idx+1]),object_path) )
                return None
            obj = obj.get(object_name)
            if obj is None:
                print("Info. Object '%s' not found (target object path is '%s')" % (".".join(object_name_list[:idx+1]),object_path) )
                return None
        return obj


if __name__== "__main__":
    #print(get_request_headers('HH','skill_set'))
    #print( get_object('HH.requests.skill_set.request_path'))
    #print(get_request_url('HH_','skill_set',{'text':'ja'}))
    #print( get_request_http_command('HH','skill_set'))
    #pprint.pprint(get_request('HH','skill_set', {'text':'ja'}))
    #pprint.pprint(get_request('HH','skill_set'))
    #pprint.pprint(get_request('HH','skill_set', text='ja'))
    #pprint.pprint(data_source)

    pprint.pprint(rest_request().create_request( 'HH','skill_set'))
    #f( 'HH','skill_set')
