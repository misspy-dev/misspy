class hook:
    functions = {}

    def add(type, func):
        hook.functions[type] = func
        return True

    def remove(type):
        hook.functions[type] = None
        return True

    def reload(type):
        func = hook.functions[type]
        hook.remove(type)
        hook.add(type, func)
        return True
