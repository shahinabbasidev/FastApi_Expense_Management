from i18n.translator import _

class Messages:
    registered_successfully = _("User has been created successfully.")
    logged_in_successfully = _("You have logged in successfully.")
    logged_out_successfully = _("You have been logged out successfully.")
    updated_successfully = _("Your profile has been updated successfully.")

    user_already_exists = _("User already exists.")
    password_missing = _("Password is required.")
    user_not_found = _("No user found with the provided details.")
    invalid_credentials =  _("Invalid username or password.")

    token_expired = _("Your session has expired. Please log in again.")
    access_token_wrong_type = _("Invalid token type. Expected an access token.")
    refresh_token_wrong_type = _("Invalid token type. Expected a refresh token.")
    token_invalid = _("Invalid authentication token.")
    token_invalid_expired = _("The token is invalid or has expired.")
    reset_link_invalid = _("The password reset link is invalid or has expired.")


    refresh_token_not_found = _("Refresh token not found.")
    token_refreshed_successfully = _("Your session has been refreshed successfully.")

    invalid_signature = _("Authentication failed, invalid signature.")
    payload_invalid = _("Authentication failed, payload invalid.")
    not_authenticated = _("NOT authenticated.")