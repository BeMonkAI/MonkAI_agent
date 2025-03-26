"""
This module is one of the key features and differentiators of the framework, designed to offer robust security through validation of access to functions. It differentiates itself by providing a validation decorator, an elegant and effective mechanism that automates the protection of sensitive functions, ensuring that only properly validated users can access them.

A crucial point is that security is not under the direct responsibility of the agents but rather managed centrally and independently. This approach ensures that protection is above the level of the agents, providing an additional layer of security and eliminating potential vulnerabilities arising from inconsistencies in the implementation of validations within the agents themselves.

The validate decorator is the module's core functionality, responsible for wrapping the protected function. It checks the user's validity before allowing the function to execute and returns a clear "access denied" message if validation fails.

Key Features:

- Simple Integration: Decorators automate validations, eliminating the need for manual checks.
- Centralized Security: Unified validation management minimizes errors and ensures consistency.
- Flexible Customization: Tailors access conditions to suit different scenarios or user roles.

"""

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
        def wrapper_validate(*args, **kwargs):
            """
            Wrapper function that performs validation before executing the original function.

            Args:
                authority: The authority object to be validated.
                *args: Variable length argument list for the original function.
                **kwargs: Arbitrary keyword arguments for the original function.

            Returns:
                The result of the original function if validation passes, otherwise a warning message.
            """
            authority = args[0] if args and hasattr(args[0], validation_func.__name__) else None
            if (authority and  validation_func(authority)) or (not authority and validation_func()) :
                logging.info("User is valid")
                return func(*args, **kwargs) 
            else:
                logging.warning("User is not validated for this functionality. Do not perform the action.")
                return "User is not validated for this functionality. Do not perform the action and notify the user thet it can not perform the action"
        
        return wrapper_validate
    return decorator_validate



