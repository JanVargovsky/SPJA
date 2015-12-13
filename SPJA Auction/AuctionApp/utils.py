def errorCheck(form):
    return [error for field in form for error in field.errors]