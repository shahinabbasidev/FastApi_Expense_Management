from i18n.translator import _


class Messages:
    @staticmethod
    def registered_successfully():
        return _("User has been created successfully.")

    @staticmethod
    def logged_in_successfully():
        return _("You have logged in successfully.")

    @staticmethod
    def logged_out_successfully():
        return _("You have been logged out successfully.")

    @staticmethod
    def updated_successfully():
        return _("Your profile has been updated successfully.")

    @staticmethod
    def user_already_exists():
        return _("User already exists.")

    @staticmethod
    def password_missing():
        return _("Password is required.")

    @staticmethod
    def user_not_found():
        return _("No user found with the provided details.")

    @staticmethod
    def invalid_credentials():
        return _("Invalid username or password.")

    @staticmethod
    def token_expired():
        return _("Your session has expired. Please log in again.")

    @staticmethod
    def access_token_wrong_type():
        return _("Invalid token type. Expected an access token.")

    @staticmethod
    def refresh_token_wrong_type():
        return _("Invalid token type. Expected a refresh token.")

    @staticmethod
    def token_invalid():
        return _("Invalid authentication token.")

    @staticmethod
    def token_invalid_expired():
        return _("The token is invalid or has expired.")

    @staticmethod
    def reset_link_invalid():
        return _("The password reset link is invalid or has expired.")

    @staticmethod
    def refresh_token_not_found():
        return _("Refresh token not found.")

    @staticmethod
    def token_refreshed_successfully():
        return _("Your session has been refreshed successfully.")

    @staticmethod
    def invalid_signature():
        return _("Authentication failed, invalid signature.")

    @staticmethod
    def payload_invalid():
        return _("Authentication failed, payload invalid.")

    @staticmethod
    def not_authenticated():
        return _("NOT authenticated.")

    @staticmethod
    def expense_not_found():
        return _("Expense not found.")

    @staticmethod
    def expense_removed_successfully():
        return _("Expense has been removed successfully.")
    
    @staticmethod
    def expense_not_found():
        return _("User not found.")
    
    @staticmethod
    def user_removed_successfully():
        return _("User has been removed successfully.")
