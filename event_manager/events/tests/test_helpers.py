def show_form_errors(response) -> None:
    """Show Form Errors from response context."""

    try:
        if "form" in response.context:
            form = response.context["form"]

            # Check if the form has errors
            if form.errors:
                print("Form Errors:", form.errors)

                # For a more detailed output, iterate through the errors
                for field, errors in form.errors.items():
                    for error in errors:
                        print(f"Error in field '{field}': {error}")
            else:
                print("No form errors found.")
        else:
            print("Form is not in the context.")
    except Exception:
        print("no form or no form errors?")
