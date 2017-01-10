from smwogger.util import get_content


class SmokeTest(object):
    def __init__(self, api, test_url=None):
        if test_url:
            self._content = get_content(test_url)['x-smoke-test']
        else:
            self._content = api.spec['x-smoke-test']
        self.api = api
        self._vars = {}

    def __call__(self, operation_id, **options):
        extra = options.get('request', {}).get('path', {})

        def _endpoint(endpoint):
            return self._path(endpoint, **extra)

        options['endpoint'] = _endpoint
        options['data_reader'] = self.set_var
        return self.api._caller(operation_id, **options)

    def scenario(self):
        return [list(step.items())[0] for step in
                self._content.get('scenario', [])]

    def _path(self, path, **extra):
        vars = dict(self._content.get('path', {}))
        vars.update(self._vars)
        vars.update(extra)
        return path.format(**vars)

    def set_var(self, name, value):
        self._vars[name] = value

    def get_var(self, name):
        return self._vars[name]
