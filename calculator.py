"""
For your homework this week, you'll be creating a wsgi application of
your own.

You'll create an online calculator that can perform several operations.

You'll need to support:

  * Addition
  * Subtractions
  * Multiplication
  * Division

Your users should be able to send appropriate requests and get back
proper responses. For example, if I open a browser to your wsgi
application at `http://localhost:8080/multiple/3/5' then the response
body in my browser should be `15`.

Consider the following URL/Response body pairs as tests:

```
  http://localhost:8080/multiply/3/5   => 15
  http://localhost:8080/add/23/42      => 65
  http://localhost:8080/subtract/23/42 => -19
  http://localhost:8080/divide/22/11   => 2
  http://localhost:8080/               => <html>Here's how to use this page...</html>
```

To submit your homework:

  * Fork this repository (Session03).
  * Edit this file to meet the homework requirements.
  * Your script should be runnable using `$ python calculator.py`
  * When the script is running, I should be able to view your
    application in my browser.
  * I should also be able to see a home page (http://localhost:8080/)
    that explains how to perform calculations.
  * Commit and push your changes to your fork.
  * Submit a link to your Session03 fork repository!


"""
import traceback
from wsgiref.simple_server import make_server


def home():
    """Gives the home page of how to use the site"""
    homepage = '''
        <h1>How to use this site:</h1>
        <p>Use this format to pick your function and values</p>
        <ul>
            <li>http://localhost:8080/multiply/3/5  => 15</li>
            <li>http://localhost:8080/add/23/42  => 65</li>
            <li>http://localhost:8080/subtract/23/42  => -19</li>
            <li>http://localhost:8080/divide/22/11 </li>
        </ul>
        '''
    return homepage


def add(*args):
    """ Returns a STRING with the sum of the arguments """

    # DONE: Fill sum with the correct value, based on the
    # args provided.
    sum = 0
    for arg in args:
        sum += int(arg)
    return str(sum)

# DONE: Add functions for handling more arithmetic operations.


def subtract(*args):
    """Returns a STRING with the difference of the arguments"""
    list_arg = list(args)
    difference = int(list_arg.pop(0))

    for arg in list_arg:
        difference -= int(arg)
    return str(difference)


def multiply(*args):
    """Returns a STRING with the product of the arguments"""
    product = 1
    for arg in args:
        product = product * int(arg)
    return str(product)


def divide(*args):
    """Returns a STRING with the quotient of the arguments"""
    quotient = 1
    for arg in args:
        quotient = quotient / int(arg)
    return str(quotient)


def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """

    # DONE: Provide correct values for func and args. The
    # examples provide the correct *syntax*, but you should
    # determine the actual values of func and args using the
    # path.
    funcs = {'': home,
             'add': add,
             'subtract': subtract,
             'multiply': multiply,
             'divide': divide}

    path = path.strip('/').split('/')
    function_name = path[0]
    args = path[1:]

    try:
        func = funcs[function_name]
    except KeyError:
        raise NameError
    return func, args


def application(environ, start_response):
    # DONE: Your application code from the book database
    # work here as well! Remember that your application must
    # invoke start_response(status, headers) and also return
    # the body of the response in BYTE encoding.
    #
    # DONE (bonus): Add error handling for a user attempting
    # to divide by zero.

    headers = [("Content-type", "text/html")]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        body = func(*args)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except ZeroDivisionError:
        status = "200 OK"
        body = "<h1>Stop trying to divide by zero! That's not how math works.<h/1>"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h1>"
        print(traceback.format_exc())
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]


if __name__ == '__main__':
    # DONE: Insert the same boilerplate wsgiref simple
    # server creation that you used in the book database.
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
