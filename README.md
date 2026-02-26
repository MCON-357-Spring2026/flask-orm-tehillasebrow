# Flask Fundamentals Exercise

## Overview

In this exercise, you'll build a simple Flask API and practice working with routes, request handling, and responses. You'll also use the `requests` library to test your API programmatically, reinforcing the client-server relationship we discussed in class.

## Learning Objectives

By the end of this exercise, you will be able to:
- Create a Flask application with multiple routes
- Handle different HTTP methods (GET, POST)
- Return different response types (HTML, JSON, custom status codes)
- Use route parameters and query strings
- Test your Flask API using the `requests` library
- Inspect Flask's URL map for debugging

## Prerequisites

- Complete the Flask introduction lesson
- Basic understanding of HTTP requests and responses

## Setup Instructions

### 1. Clone and Setup Your Repository
```bash
# Clone your GitHub Classroom repository
git clone <your-repo-url>
cd <repo-name>

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Verify Installation
from terminal, run:
```bash
python -c "import flask; print(flask.__version__)"
```
## Part 1: Building Your Flask API  - In class exercise

Create a file called `app.py` in your repository and implement the following routes:

### Route 1: Welcome Endpoint
- **URL:** `/`
- **Method:** GET
- **Response:** Return an HTML string with a welcome message
- **Example:** `<h1>Welcome to My Flask API!</h1>`

### Route 2: About Endpoint
- **URL:** `/about`
- **Method:** GET
- **Response:** Return JSON with information about yourself
- **Example:** `{"name": "Your Name", "course": "MCON-504 - Backend Development", "semester": "Spring 2025"}`

**Hint:** Use `jsonify()` from Flask to return JSON responses.

### Route 3: Greeting with Name Parameter
- **URL:** `/greet/<name>`
- **Method:** GET
- **Response:** Return a personalized greeting using the name from the URL
- **Example:** When accessing `/greet/Lila`, return `<p>Hello, Lila! Welcome to Flask.</p>`

### Route 4: Calculator Endpoint
- **URL:** `/calculate`
- **Method:** GET
- **Query Parameters:** `num1`, `num2`, `operation`
- **Response:** Return JSON with the calculation result
- **Operations:** Support `add`, `subtract`, `multiply`, `divide`
- **Example:** `/calculate?num1=10&num2=5&operation=add` returns `{"result": 15, "operation": "add"}`

**Hint:** Access query parameters using `request.args.get('parameter_name')`

### Route 5: Echo Endpoint (POST)
- **URL:** `/echo`
- **Method:** POST
- **Request Body:** JSON data
- **Response:** Return the same JSON data back with an additional field `"echoed": true`
- **Example:** If you POST `{"message": "Hello"}`, return `{"message": "Hello", "echoed": true}`

**Hint:** Use `request.get_json()` to parse JSON from the request body.

### Route 6: Status Code Practice
- **URL:** `/status/<int:code>`
- **Method:** GET
- **Response:** Return a message with the specified HTTP status code
- **Example:** `/status/404` returns `"This is a 404 error"` with status code 404

**Hint:** Return a tuple: `(message, status_code)`

### Running Your Flask App

Add this to the bottom of your `app.py`:
```python
if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

Run your application:
```bash
python app.py
```

Or use the Flask CLI:
```bash
flask --app app run --debug
```
In the end of the class submit app.py to your GitHub repository.
Make sure to test each route in your browser or using a tool like Postman to ensure they work as expected.
To submit run from terminal
```bash
git add app.py
git commit -m "Implement Flask API routes"
git push origin main
```


### Part 2 - Homework 
Hooks and testing are important parts of Flask development. For homework, implement the following:

Add a route that demonstrates using `before_request` hook:
- Create a `before_request` function that logs the request method and path to the console
- Add it to your Flask app using the `@app.before_request` decorator

Add a route that demonstrates using `after_request` hook:
- Create an `after_request` function that adds a custom header `X-Custom-Header: FlaskRocks` to every response
- Add it to your Flask app using the `@app.after_request` decorator
- Test that the custom header is present in the response when you access any route

Add a route that demonstrates using `teardown_request` hook:
- Create a `teardown_request` function that logs any exceptions that occur during request handling
- Add it to your Flask app using the `@app.teardown_request` decorator
  - Test that the teardown function is called by intentionally causing an error in one of your routes (e.g., by dividing by zero in the calculator route) and checking the console logs for the exception
  - Make sure to handle the exception properly in your route so that it doesn't crash the server, but still allows you to see the error in the logs.
  - Example of handling the exception in the calculator route:
    - ```python
      @app.route('/calculate')
      def calculate():
          num1 = float(request.args.get('num1', 0))
          num2 = float(request.args.get('num2', 0))
          operation = request.args.get('operation')
          try:
              if operation == 'add':
                  result = num1 + num2
              elif operation == 'subtract':
                  result = num1 - num2
              elif operation == 'multiply':
                  result = num1 * num2
              elif operation == 'divide':
                  result = num1 / num2
              else:
                  return jsonify({"error": "Invalid operation"}), 400
              return jsonify({"result": result, "operation": operation})
          except Exception as e:
              # Log the exception and return an error response
              print(f"Error occurred: {e}")
              return jsonify({"error": "An error occurred during calculation"}), 500
      ```

    
## Part 2: Testing with the Requests Library (15 minutes)

Create a file called `test_api.py` that uses the `requests` library to test your Flask API.

### Your Test Script Should:

1. **Test the Welcome Route**
```python
   response = requests.get('http://localhost:5000/')
   print(f"Status Code: {response.status_code}")
   print(f"Content: {response.text}")
```

2. **Test the About Route**
    - Make a GET request to `/about`
    - Parse the JSON response
    - Print the values

3. **Test the Greeting Route**
    - Make a request with your name in the URL
    - Verify the response contains your name

4. **Test the Calculator Route**
    - Test at least two different operations
    - Print the results
    - Handle the case where division by zero might occur

5. **Test the Echo Route (POST)**
    - Send JSON data using `requests.post()`
    - Verify the response includes `"echoed": true`

6. **Test Different Status Codes**
    - Request at least two different status codes
    - Print both the status code and response text
7. **Test Custom Headers**
    - Make a request to any route
    - Verify that the response includes the `X-Custom-Header: FlaskRocks` header
    - Print the value of the custom header from the response
    - Example:
    ```python
    response = requests.get('http://localhost:5000/')
    custom_header = response.headers.get('X-Custom-Header')
    print(f"Custom Header: {custom_header}")
    ```
8. **Test Error Handling**
    - Intentionally cause an error (e.g., division by zero in the calculator route)
    - Verify that the error is handled gracefully and that the appropriate error message and status code are returned
    - Example:
    ```python
        response = requests.get('http://localhost:5000/calculate?num1=10&num2=0&operation=divide')
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")

      ```

### Running Your Tests

Make sure your Flask app is running in one terminal, then in another terminal:
```bash
python test_api.py
```

## Part 3: Reflection and Debugging (10 minutes)

### Inspect Your URL Map

Add this debug route to your `app.py`:
```python
@app.route('/debug/routes')
def show_routes():
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append({
            'endpoint': rule.endpoint,
            'methods': list(rule.methods),
            'path': str(rule)
        })
    return jsonify(routes)
```

Visit `http://localhost:5000/debug/routes` to see all your registered routes.

### Answer These Questions

Create a file called `REFLECTION.md` and answer:

1. What does the `@app.route()` decorator actually do?
2. How does Flask know which function to call when a request arrives?
3. What's the difference between route parameters (`<name>`) and query parameters (`?key=value`)?
4. Why do we need to use `request.get_json()` for POST requests but `request.args.get()` for GET query parameters?
5. What happens if you try to access `request.args` outside of a request context?

## Submission Checklist

Before you submit, make sure you have:

- [ ] `app.py` with all routes implemented 
- [ ] `test_api.py` with tests for all your routes
- [ ] `REFLECTION.md` with answers to the questions
- [ ] All files committed and pushed to your GitHub repository
- [ ] Tested that your Flask app runs without errors
- [ ] Verified that your test script successfully calls all endpoints

## Submission
```bash
git add .
git commit -m "Complete Flask fundamentals homework"
git push origin main
```

## Common Issues and Troubleshooting

### Flask app won't start
- Make sure you're in your virtual environment
- Check that Flask is installed: `pip list | grep Flask`
- Ensure no other process is using port 5000

### Requests library can't connect
- Make sure your Flask app is actually running
- Verify you're using the correct URL: `http://localhost:5000`
- Check that you haven't changed the default port

### JSON parsing errors
- Use `request.get_json()` for POST request bodies
- Use `request.args.get()` for query parameters
- Use `jsonify()` to return JSON responses

### Import errors
- Make sure you've activated your virtual environment
- Reinstall requirements: `pip install -r requirements.txt`

## Resources
- [Flask Web Development](https://coddyschool.com/upload/Flask_Web_Development_Developing.pdf)
- [Flask Quickstart Documentation](https://flask.palletsprojects.com/en/stable/quickstart/)
- [Requests Library Documentation](https://requests.readthedocs.io/en/latest/)
- [Flask Request Object](https://flask.palletsprojects.com/en/stable/api/#flask.Request)
- [HTTP Status Codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)

## Grading Rubric

| Component | Points |
|-----------|--------|
| All 6 routes implemented correctly | 40 |
| Test script covers all endpoints | 30 |
| Code quality and organization | 15 |
| Reflection questions answered | 15 |
| **Total** | **100** |

---

**Questions?** Post in the class discussion board or attend office hours.

**Need Help?** Remember to check:
1. The lesson materials
2. Flask error messages (they're usually helpful!)
3. Ask your teacher or classmates for hints (but try to solve it yourself first!)
4. Use online resources like Flask documentation
Good luck! 