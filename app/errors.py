from flask import Blueprint, render_template

app = Blueprint("errors", __name__)


# Error handler for 404 (Path Not Found Error) errors
@app.errorhandler(404)
def page_not_found(error):
    return render_template("not_found.html"), 404


# Error handler for 400 errors
@app.errorhandler(400)
def bad_request(error):
    return render_template("bad_request.html", error=error), 400


# Error handler for 401 errors
@app.errorhandler(401)
def unauthorized(error):
    return render_template("unauthorized.html", error=error), 401


# Error handler for 403 errors
@app.errorhandler(403)
def forbidden(error):
    return render_template("forbidden.html", error=error), 403


# Error handler for 405 errors
@app.errorhandler(405)
def method_not_allowed(error):
    return render_template("method_not_allowed.html", error=error), 405


# Error handler for 406 errors
@app.errorhandler(406)
def not_acceptable(error):
    return render_template("not_acceptable.html", error=error), 406


# Error handler for 415 errors
@app.errorhandler(415)
def unsupported_media_type(error):
    return render_template("unsupported_media_type.html", error=error), 415


# Error handler for 422 errors
@app.errorhandler(422)
def unprocessable_entity(error):
    return render_template("unprocessable_entity.html", error=error), 422


# Error handler for 429 errors
@app.errorhandler(429)
def too_many_requests(error):
    return render_template("too_many_requests.html", error=error), 429


# Error handler for 500 errors
@app.errorhandler(500)
def internal_server_error(error):
    return render_template("internal_error.html", error=error), 500


# Error handler for 503 errors
@app.errorhandler(503)
def service_unavailable(error):
    return render_template("service_unavailable.html", error=error), 503
