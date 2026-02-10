from i18n.translator import _

class Messages:
    registered_successfully = _("Your account has been created successfully.")
    logged_in_successfully = _("You have logged in successfully.")
    logged_out_successfully = _("You have been logged out successfully.")

    user_already_exists = _("An account with this email already exists.")
    password_missing = _("Password is required.")
    user_not_found = _("No user found with the provided details.")
    invalid_credentials =  _("Invalid email or password.")

    token_expired = _("Your session has expired. Please log in again.")
    token_invalid = _("Invalid authentication token.")
    token_invalid_expired = _("The token is invalid or has expired.")
    reset_link_invalid = _("The password reset link is invalid or has expired.")


    refresh_token_not_found = _("Refresh token not found.")
    token_refreshed_successfully = _("Your session has been refreshed successfully.")

    