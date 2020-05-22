class Bundle:
    __common_paths = []
    __base_path = ''

    def __init__(self, base_path: str = '/rest/', common_paths=None):
        if common_paths is None:
            common_paths = ['api/2/', 'auth/1/', 'agile/1.0/']
        self.__common_paths = common_paths
        self.__base_path = base_path

    def pack(self, resources: list) -> dict:
        packed = {}
        for resource in resources:
            endpoint_name = resource['uri']
            resource_path = self.__base_path + resource['uri']
            for common_path in self.__common_paths:
                endpoint_name = endpoint_name.replace(common_path, '')
            endpoint_name = endpoint_name.split('/', maxsplit=1)[0]
            # /api/2 resource
            if endpoint_name == '':
                endpoint_name = 'Api2'
            self.__patch_root_methods(resource, resource_path)
            if packed.get(endpoint_name) is None:
                packed[endpoint_name] = []
            if resource.get('methods'):
                packed[endpoint_name] += resource['methods']
            if resource.get('sub_resources'):
                for sub_resource in resource['sub_resources']:
                    sub_resource_path = self.__base_path + sub_resource['uri']
                    self.__patch_sub_methods(sub_resource, sub_resource_path)
                    if sub_resource.get('methods'):
                        packed[endpoint_name] += sub_resource['methods']
        for endpoint in packed.keys():
            packed[endpoint] = sorted(packed[endpoint], key=lambda method: method['id'])
        return packed

    @staticmethod
    def __patch_root_methods(resource: dict, path: str):
        if resource.get('methods') is None:
            return
        for method in resource['methods']:
            method['path'] = path
            if resource.get('parameters'):
                method['parameters'] = resource['parameters']

    @staticmethod
    def __patch_sub_methods(sub_resource: dict, path: str):
        if sub_resource.get('methods') is None:
            return
        for method in sub_resource['methods']:
            method['path'] = path
            if sub_resource.get('parameters'):
                method['parameters'] = sub_resource['parameters']
