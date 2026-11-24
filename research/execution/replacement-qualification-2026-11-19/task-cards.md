# Account extension tasks

Implement the requested change in the supplied repository. Keep the supplied layout, dependencies, and public routes. Study accounts and application records are synthetic.

## Display-name normalization

When a signed-in user saves a new display name in account settings, remove leading and trailing whitespace before storing the name. Preserve whitespace inside the name. For example, saving `  Mai  Linh  ` stores `Mai  Linh`. Reloading settings shows the stored name. Opening settings without editing must show an existing name exactly as stored, including leading and trailing whitespace in legacy names. Preserve the existing account identity, permissions, and unrelated settings.

## Sign-out confirmation

Add a native browser confirmation dialog to the existing dashboard sign-out control. Cancel must preserve the current session, including when the control is activated by keyboard. Confirm performs the existing sign-out operation and follows the kit's existing navigation behavior. After it completes, a fresh request in the same browser session to a protected account page must require sign-in. Preserve ordinary sign-in and the existing access restriction for unauthenticated visitors.

## Sign-in password visibility

Add a keyboard-operable button to reveal or mask the password on the sign-in form. Name it “Show password” when masked and “Hide password” when revealed. Toggling must retain the current input value and must not submit the form. Keep the field masked when the sign-in page first opens. Preserve ordinary sign-in, masking in the sign-up form, and the existing autocomplete behavior.
