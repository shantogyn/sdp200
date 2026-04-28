"""
Validation Module
Provides validation functions for user input and data
"""

import re
from typing import Tuple

class Validator:
    """Class containing validation methods"""
    
    @staticmethod
    def validate_username(username: str) -> Tuple[bool, str]:
        """
        Validate username format
        Args:
            username: Username to validate
        Returns:
            Tuple of (is_valid, message)
        """
        if not username or len(username) < 3:
            return False, "Username must be at least 3 characters long"
        
        if len(username) > 100:
            return False, "Username must not exceed 100 characters"
        
        if not re.match("^[a-zA-Z0-9_]+$", username):
            return False, "Username can only contain letters, numbers, and underscores"
        
        return True, "Valid username"
    
    @staticmethod
    def validate_email(email: str) -> Tuple[bool, str]:
        """
        Validate email format
        Args:
            email: Email to validate
        Returns:
            Tuple of (is_valid, message)
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if not email:
            return False, "Email cannot be empty"
        
        if not re.match(pattern, email):
            return False, "Invalid email format"
        
        return True, "Valid email"
    
    @staticmethod
    def validate_password(password: str) -> Tuple[bool, str]:
        """
        Validate password strength
        Args:
            password: Password to validate
        Returns:
            Tuple of (is_valid, message)
        """
        if not password or len(password) < 6:
            return False, "Password must be at least 6 characters long"
        
        if len(password) > 255:
            return False, "Password is too long"
        
        # Check for at least one uppercase, one lowercase, one digit
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        
        if not (has_upper and has_lower and has_digit):
            return False, "Password must contain uppercase, lowercase, and numbers"
        
        return True, "Strong password"
    
    @staticmethod
    def validate_age(age: str) -> Tuple[bool, str]:
        """
        Validate age input
        Args:
            age: Age value to validate
        Returns:
            Tuple of (is_valid, message)
        """
        try:
            age_int = int(age)
            if age_int < 1 or age_int > 150:
                return False, "Age must be between 1 and 150"
            return True, "Valid age"
        except ValueError:
            return False, "Age must be a number"
    
    @staticmethod
    def validate_weight(weight: str) -> Tuple[bool, str]:
        """
        Validate weight input
        Args:
            weight: Weight value to validate
        Returns:
            Tuple of (is_valid, message)
        """
        try:
            weight_float = float(weight)
            if weight_float < 20 or weight_float > 300:
                return False, "Weight must be between 20 and 300 kg"
            return True, "Valid weight"
        except ValueError:
            return False, "Weight must be a number"
    
    @staticmethod
    def validate_height(height: str) -> Tuple[bool, str]:
        """
        Validate height input
        Args:
            height: Height value to validate
        Returns:
            Tuple of (is_valid, message)
        """
        try:
            height_float = float(height)
            if height_float < 100 or height_float > 250:
                return False, "Height must be between 100 and 250 cm"
            return True, "Valid height"
        except ValueError:
            return False, "Height must be a number"
    
    @staticmethod
    def validate_not_empty(value: str, field_name: str) -> Tuple[bool, str]:
        """
        Validate that field is not empty
        Args:
            value: Value to validate
            field_name: Name of the field for error message
        Returns:
            Tuple of (is_valid, message)
        """
        if not value or len(value.strip()) == 0:
            return False, f"{field_name} cannot be empty"
        return True, "Valid"
