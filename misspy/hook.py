class hook:
    
    functions = {}

    def add(event, func):
        
        """add

        Args:
            event (str): streaming event type. (view docs)
            func (funct): Function to call on events entered in event

        Returns:
            bool: True
        """

        hook.functions[event] = func
        return True

    def remove(event):
        """remove

        Args:
            event (str): streaming event type. (view docs)

        Returns:
            bool: True
        """
        
        hook.functions[event] = None
        return True

    def reload(event):
        """reload

        Internally, it just executes remove and add.
        
        Args:
            event (str): streaming event type. (view docs)

        Returns:
            bool: True
        """
        
        func = hook.functions[event]
        hook.remove(event)
        hook.add(event, func)
        return True