import json
import os
import requests
import yaml

action_order = ["$filter", "$search", "$items", "$foreach"]


class Entities():
    pass


class Swagger(object):

    def __init__(self, swagger):
        self.basePath = swagger["basePath"]
        self.host = swagger["host"]
        self.scheme = swagger.get("schemes", ["http"])[0]
        self.uri = self.scheme + "://" + swagger["host"]
        if swagger["basePath"] != "/":
            self.uri += swagger["basePath"]
        self.securityHeaders = []
        self.paths = paths = swagger["paths"]
        self.definitions = swagger.get("definitions", {})
        if swagger.get("securityDefinitions"):
            for sec in swagger["securityDefinitions"]:
                if swagger["securityDefinitions"][sec]["type"] == "apiKey":
                    if swagger["securityDefinitions"][sec]["in"] == "header":
                        name = swagger["securityDefinitions"][sec]["name"]
                        self.securityHeaders.append(name)

        for path in paths:
            for method in paths[path]:
                opid = paths[path][method]["operationId"]
                setattr(self, opid, ApiRequest(self.uri + path, method,
                                               paths[path][method],
                                               self.definitions,
                                               self.securityHeaders))


class ApiRequest(object):

    def __init__(self, path, method, data, definitions, security=None):

        if security is None:
            security = []

        self.path = path
        self.method = method
        self.data = data
        self.header_params = []
        self.path_params = []
        self.query_params = []
        self.body_params = []
        self.required_params = []
        self.parameters = []
        self.id = data["operationId"]
        if data.get("parameters"):
            for param in data["parameters"]:
                name = param["name"]
                place = param["in"]
                if place == "header":
                    self.parameters.append(name)
                    if param.get("required"):
                        self.required_params.append(name)
                    self.header_params.append(name)
                if place == "query":
                    self.parameters.append(name)
                    if param.get("required"):
                        self.required_params.append(name)
                    self.query_params.append(name)
                if place == "path":
                    self.parameters.append(name)
                    self.required_params.append(name)
                    self.path_params.append(name)
                if place == "body":
                    if param["schema"].get("$ref"):
                        body_params = definitions[
                            param["schema"]["$ref"].split("/")[2]]
                    else:
                        body_params = param["schema"]
                    required = body_params.get("required", [])
                    for p in body_params["properties"]:
                        self.parameters.append(name)
                        if p in required:
                            self.required_params.append(p)
                        self.body_params.append(p)
        if data.get("security") == {}:
            pass
        else:
            self.header_params.extend(security)
            self.parameters.extend(security)
            self.required_params.extend(security)

    def __call__(self, *args, **kwargs):
        headers = {}
        data = {}
        query = {}
        print kwargs.keys()
        for p in self.required_params:
            if kwargs.get(p) == None:
                raise Exception("Parameter {0} missing".format(p))
        for h in self.header_params:
            if kwargs.get(h):
                headers[h] = kwargs[h]
        for d in self.body_params:
            if kwargs.get(d):
                data[d] = kwargs[d]
        for q in self.query_params:
            if kwargs.get(q):
                query[q] = kwargs[q]

        uri = self.path.format(*args, **kwargs)
        print self.method, uri, query, headers, data
        response = requests.request(
            self.method, uri, params=query, headers=headers,
            data=json.dumps(data), verify=False)
        if response.ok:
            try:
                return response.json()
            except:
                return {"response": response.content}
        else:
            raise Exception(response.content)


class Helpers(object):

    def _get_config(self,):
        pass

    def _type(self, param_name, param_type, **kwargs):
        types = {
            str: "string",
            int: "integer",
            bool: "boolean",
            unicode: "string"
        }
        param = kwargs.get(param_name)
        if param:
            if types.get(type(param)) == param_type:
                return kwargs
            else:
                problem = "Parameter {0} should be of type {1}".format(
                    param_name,
                    param_type)
                raise Exception(problem)
        return kwargs

    def _file(self, param_name, input_name, **kwargs):
        file_path = kwargs.get(input_name)
        if file_path:
            if not os.path.isfile(file_path):
                raise Exception(
                    file_path, "is not a file or could not be found in the\
                                given path")

            with open(file_path) as f:
                opened_file = f.read()

            kwargs.pop(input_name)
            kwargs[param_name] = opened_file
        return kwargs

    def _ref(self, param_name, input_name, **kwargs):
        if input_name == "$body":
            kwargs[param_name] = kwargs
            return kwargs

        input_value = kwargs.get(input_name)

        if input_value != None:
            kwargs[param_name] = input_value
            kwargs.pop(input_name)
            return kwargs
        return kwargs

    def _ref_first(self, param_name, input_name, **kwargs):
        input_value = kwargs.get(input_name)
        if input_value and isinstance(input_value, list):
            kwargs[param_name] = input_value[0]
            kwargs.pop(input_name)
            return kwargs
        return kwargs

    def _default(self, param_name, default_value, **kwargs):
        input_value = kwargs.get(param_name)
        if not input_value:
            kwargs[param_name] = default_value
            return kwargs
        return kwargs

    def _exists(self, param_name, exists, **kwargs):
        param = kwargs.get(param_name, False)
        if exists and param:
            return True
        if not exists and not param:
            return True
        return False

    def _set(self, input_name, property_name, **kwargs):
        if kwargs.get("$response"):
            kwargs = kwargs["$response"]
        if input_name == "$body":
            setattr(self, property_name, kwargs)
        else:
            setattr(self, property_name, kwargs.get(input_name))
        return True

    def _in(self, param_name, enum, **kwargs):
        param = kwargs.get(param_name)
        if param and param in enum:
            return True
        return False

    def _eq(self, param_name, value, **kwargs):
        param = kwargs.get(param_name)
        if param and param == value:
            return True
        return False

    def _required(self, param_name, value, **kwargs):
        if kwargs.get(param_name):
            return kwargs
        problem = "Parameter {0} is required".format(param_name)
        raise Exception(problem)

    def _get_valid_case(self, cases, **kwargs):
        for case in cases:
            if self._check_case(case["case"], **kwargs):
                return case
        valid_cases = json.dumps(
            cases, sort_keys=True, indent=4, separators=(',', ': '))
        problem = "Every `case` in `init` was found invalid."
        problem += "Valid cases are: {0}".format(valid_cases)
        raise Exception(problem)

    def _init(self, _case, **kwargs):
        action = _case.get("action", None)
        for attr in self._attributes:
            if hasattr(self, attr):
                kwargs[attr] = getattr(self, attr)
        response_schema = _case.get("response", {})
        if isinstance(action, basestring):
            funcact = getattr(self._spec, action)
            response = funcact(**kwargs)
            for param_name in response_schema:
                schema = response_schema[param_name]
                if isinstance(response, (list, basestring)):
                    response = {"$response": response}
                for action in schema:
                    if not self._run(action, param_name, schema[action],
                                     **response):
                        problem = "Action {0} with parameters {1},{2} failed to\
                                   execute!".format(action, param_name,
                                                    schema[action])
                        raise Exception(problem)
            return True
        elif isinstance(action, list):
            pass
        elif isinstance(action, dict):
            pass
        else:
            return True

    def _set_from_config(self, _property_name, _config_key, **kwargs):
        if self._config.get(_config_key):
            setattr(self, _property_name, self._config[_config_key])
            return True
        return False

    def _filter(self, _keys, _response, **kwargs):
        for key in _keys:
            query = kwargs.get(key)
            if query:
                return [item for item in _response if item.get(key) == query]
        return _response

    def _search(self, _search_query, _response, **kwargs):

        value = kwargs.get(_search_query)
        if not value:
            return _response
        answer = []
        for item in _response:
            if isinstance(item, basestring):
                item = _response[item]
            stritem = json.dumps(item)
            if value in stritem:
                answer.append(item)
        return answer

    def _items(self, _items, _response, **kwargs):
        answer = []
        for action in _items:
            for item in _response:
                item = self._run(action, _items[action], item, **kwargs)
                answer.append(item)
        return answer

    def _entity(self, _item, _data, **kwargs):
        ent = getattr(Entities, _item)
        for attr in ent._attributes:
            if not _data.get(attr):
                if hasattr(self, attr):
                    _data[attr] = getattr(self, attr)
                elif kwargs.get(attr):
                    _data[attr] = kwargs[attr]

        return ent(**_data)

    def _foreach(self, _items, _response, **kwargs):
        answer = []
        for action in _items:
            for item in _response:
                item = self._run(action, _items[action], item, **kwargs)
                answer.extend(item)
        return answer

    def _method(self, _action, _data, **kwargs):
        method = getattr(_data, _action)
        return method(**kwargs)

    def _check_case(self, _case, **kwargs):
        case = _case.get('$if')

        if case:
            for param in case:
                for check in case[param]:
                    valid = self._run(check, param, case[
                                      param][check], **kwargs)
                    if not valid:
                        return False
            return True
        else:
            return True

    def _run(self, _helper, _parent, _value, **kwargs):
        if _helper.startswith("$"):
            return getattr(self, _helper.replace("$", "_"))(_parent, _value,
                                                            **kwargs)


class Client(object):

    def __init__(self, url="", basepath="api", modelname="model"):
        if url:
            modelurl = "{0}/{1}/{2}.yaml".format(url, basepath, modelname)
            response = requests.get(modelurl)
            self.model = yaml.load(response.content)
        else:
            path = os.path.realpath(__file__)
            path = os.path.dirname(path)
            path = os.path.join(path, basepath, modelname + ".yaml")
            print path
            if os.path.isfile(path):
                f = open(path)
                self.model = yaml.load(f.read())
            else:
                raise Exception("Model file not found in {0}".format(path))
        self.root = self.model.get("root")
        api_spec = self.model.get("api-spec")
        if url:
            specurl = "{0}/{1}/{2}.yaml".format(url, basepath, api_spec)
            response = requests.get(specurl)
            self.spec = Swagger(yaml.load(response.content))
        else:
            path = os.path.realpath(__file__)
            path = os.path.dirname(path)
            path = os.path.join(path, basepath, api_spec + ".yaml")
            if os.path.isfile(path):
                f = open(path)
                self.spec = Swagger(yaml.load(f.read()))
            else:
                raise Exception("Swagger spec file not found in {0}".format(path))
        if self.model.get("config_path"):
            home_path = os.getenv("HOME")
            save_path = self.model["config_path"]
            self.__config_path = os.path.join(home_path, "." + save_path)
            if os.path.isfile(self.__config_path):
                with open(self.__config_path) as f:
                    self.__config = yaml.load(f.read())
            else:
                self.__config = {}
                self.__config_path = ""
        else:
            self.__config = {}
            self.__config_path = ""

    def __call__(self, entity=None):
        if entity is None:
            entity = self.root
            Entity = self.model["entities"][entity]
        else:
            Entity = self.model["entities"][entity]
        parameters = Entity.get("parameters", {})
        init_cases = Entity.get("init")
        properties = Entity.get("_properties")
        attributes = Entity.get("attributes", [])
        prepare_steps = Entity.get("prepare")
        methods = Entity.get("methods", {})
        config = self.__config
        config_path = self.__config_path
        spec = self.spec
        tempent = {}
        tempent["_parameters"] = parameters
        tempent["_attributes"] = attributes
        tempent["_config"] = config
        tempent["_config_path"] = config_path
        tempent["_spec"] = spec
        tempent["_init_cases"] = init_cases
        tempent["_prepare_steps"] = prepare_steps
        cls = type(entity, (Helpers, object), tempent)

        def init(self, entity=Entity, **kwargs):
            parameters = self._parameters
            for param_name in parameters:
                for action in parameters[param_name]:
                    value = parameters[param_name][action]
                    kwargs = self._run(action, param_name, value, **kwargs)
            for p in attributes:
                value = kwargs.get(p)
                if value:
                    setattr(self, p, value)
            if self._init_cases:
                case = self._get_valid_case(init_cases, **kwargs)
                self._init(case["case"], **kwargs)
            if self._prepare_steps:
                for step in self._prepare_steps:
                    if self._check_case(step["step"]):
                        self._init(step["step"], **kwargs)

        setattr(cls, "__init__", init)
        if properties:
            setattr(cls, "_properties", properties)

            def _getattr_(self, name):
                try:
                    return object.__getattribute__(self, name)
                except:
                    if self._properties.get(name):
                        self._init(self._properties[name])
                        del self._properties[name]
                    return object.__getattribute__(self, name)

            setattr(cls, "__getattribute__", _getattr_)
        for method_name in methods:
            method = methods[method_name]

            def decorated_method(self, _method=method, _name=method_name,
                                 *args, **kwargs):
                method = _method
                action = method.get("action")
                parameters = method.get("parameters", {})
                switch_cases = method.get("switch")
                response_schema = method.get("response", {})
                for attr in self._attributes:
                    kwargs[attr] = getattr(self, attr)
                for param_name in parameters:
                    for act in parameters[param_name]:
                        value = parameters[param_name][act]
                        kwargs = self._run(act, param_name, value, **kwargs)
                if switch_cases:
                    case = self._get_valid_case(switch_cases, **kwargs)
                    if case.get("action"):
                        self._init(case, **kwargs)
                funcact = getattr(self._spec, action)
                response = funcact(**kwargs)
                for act in action_order:
                    if act in response_schema:
                        response = self._run(act, response_schema[
                                             act], response, **kwargs)

                for act in response_schema:
                    if not act.startswith("$"):
                        for act2 in response_schema[act]:
                            self.run(act2, act, response[
                                     act][act2], **response)
                return response
            decorated_method.__name__ = method_name
            decorated_method.func_name = method_name
            setattr(cls, method_name, decorated_method)
        if not entity == self.root:
            return cls
        for ent in self.model["entities"]:
            if ent != self.root:
                entcls = Client.__call__(self, ent)
                setattr(Entities, ent, entcls)

        return cls


newcls = Client()
MistClient = newcls()
