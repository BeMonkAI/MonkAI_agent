import logging
import functools

def validate(validation_func):
    def decorator_validate(func):
        """
        Decorator to validate user authority before executing a function.

        Args:
            validation_func (Callable): A function that takes an authority argument and returns a boolean indicating whether the user is validated.

        Returns:
            Callable: A decorator that wraps the original function with validation logic.
        """
        @functools.wraps(func)
        def wrapper_validate(authority, *args, **kwargs):
            """
            Wrapper function that performs validation before executing the original function.

            Args:
                authority: The authority object to be validated.
                *args: Variable length argument list for the original function.
                **kwargs: Arbitrary keyword arguments for the original function.

            Returns:
                The result of the original function if validation passes, otherwise a warning message.
            """
            if validation_func(authority):
                logging.info("User is valid")
                return func(authority, *args, **kwargs)
            else:
                logging.warning("User is not validated for this functionality. Do not perform the action.")
                return "User is not validated for this functionality. Do not perform the action."
        
        return wrapper_validate
    return decorator_validate



