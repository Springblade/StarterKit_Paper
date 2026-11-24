# Account extension task

Implement the requested change in the supplied repository. Keep the behavior required below, the existing layout, and the installed dependencies. All accounts and app data in the study runtime are synthetic.

## Registration password minimum

Require at least 12 characters at registration, including enforcement on the server. A password of 11 ASCII characters must be rejected without creating an account; a valid password of 12 ASCII characters must be accepted. Preserve the existing email-verification and automatic sign-in behavior of the kit. Existing accounts with valid passwords below the new threshold must still be able to sign in. Preserve the kit's existing maximum and password-change, reset, and unrelated workflows.

## Sign-out confirmation

Add confirmation to the existing dashboard sign-out control. In this task, use the browser's confirmation dialog so the check can exercise the same interaction across kits. Cancel keeps the current authenticated session and can be invoked after activating the control by mouse or keyboard. Confirm performs the existing sign-out operation and leaves the user at the kit's usual signed-out destination. After confirmation, a fresh request in that browser session to the dashboard must require sign-in. Ordinary sign-in and unauthenticated dashboard access restrictions must be preserved.

## Sign-in password visibility

Add a keyboard-operable button to reveal or mask the password on the sign-in form. Name it “Show password” when masked and “Hide password” when revealed. Toggling must preserve the input value and must not submit the form. On a fresh sign-in page, keep the password masked. Preserve ordinary sign-in, the sign-up form's password masking, and the input's password-manager autocomplete behavior.
