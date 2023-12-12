class cmdHook:
    functions = {}

    def add_hook(event, func):
        """add

        Args:
            event (str): streaming event type. (view docs)
            func (funct): Function to call on events entered in event

        Returns:
            bool: True
        """

        cmdHook.functions[event] = func
        return True

    def remove_hook(event):
        """remove

        Args:
            event (str): streaming event type. (view docs)

        Returns:
            bool: True
        """
        
        cmdHook.functions[event] = None
        return True

    def reload_hook(event):
        """reload

        Internally, it just executes remove and add.
        
        Args:
            event (str): streaming event type. (view docs)

        Returns:
            bool: True
        """
        
        func = cmdHook.functions[event]
        cmdHook.remove(event)
        cmdHook.add(event, func)
        return True