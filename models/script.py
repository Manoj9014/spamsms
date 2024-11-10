import os


def setup_project_structure():
    # Get the current directory
    current_dir = os.getcwd()

    # Create templates directory if it doesn't exist
    templates_dir = os.path.join(current_dir, 'templates')
    if not os.path.exists(templates_dir):
        os.makedirs(templates_dir)
        print(f"Created templates directory at: {templates_dir}")

    # Create models directory if it doesn't exist
    models_dir = os.path.join(current_dir, 'models')
    if not os.path.exists(models_dir):
        os.makedirs(models_dir)
        print(f"Created models directory at: {models_dir}")

    # Create index.html in templates directory
    index_html_path = os.path.join(templates_dir, 'index.html')
    if not os.path.exists(index_html_path):
        with open(index_html_path, 'w') as f:
            f.write("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Spam Detection System</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        h1 {
            color: #333;
            text-align: center;
        }
        textarea {
            width: 100%;
            padding: 10px;
            margin: 10px 0;
            border: 1px solid #ddd;
            border-radius: 4px;
            min-height: 100px;
            resize: vertical;
        }
        button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            width: 100%;
            font-size: 16px;
        }
        button:hover {
            background-color: #45a049;
        }
        #result {
            margin-top: 20px;
            padding: 15px;
            border-radius: 4px;
            display: none;
        }
        .spam {
            background-color: #ffebee;
            border: 1px solid #ffcdd2;
        }
        .not-spam {
            background-color: #e8f5e9;
            border: 1px solid #c8e6c9;
        }
        .error {
            background-color: #fff3e0;
            border: 1px solid #ffe0b2;
        }
        .loader {
            display: none;
            text-align: center;
            margin: 10px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Spam Detection System</h1>
        <form id="spam-form">
            <textarea name="message" placeholder="Enter your message here..." required></textarea>
            <button type="submit">Check for Spam</button>
        </form>
        <div class="loader">
            Analyzing message...
        </div>
        <div id="result"></div>
    </div>

    <script>
        $(document).ready(function() {
            $('#spam-form').on('submit', function(e) {
                e.preventDefault();

                const message = $('textarea[name="message"]').val();
                if (!message) {
                    $('#result')
                        .html('Please enter a message')
                        .removeClass('spam not-spam')
                        .addClass('error')
                        .show();
                    return;
                }

                $('.loader').show();
                $('#result').hide();

                $.ajax({
                    url: '/predict',
                    method: 'POST',
                    data: $(this).serialize(),
                    success: function(response) {
                        $('.loader').hide();
                        if (response.error) {
                            $('#result')
                                .html(response.error)
                                .removeClass('spam not-spam')
                                .addClass('error')
                                .show();
                        } else {
                            const resultClass = response.prediction === 'Spam' ? 'spam' : 'not-spam';
                            $('#result')
                                .html(`Prediction: <strong>${response.prediction}</strong><br>Confidence: ${response.confidence}`)
                                .removeClass('spam not-spam error')
                                .addClass(resultClass)
                                .show();
                        }
                    },
                    error: function() {
                        $('.loader').hide();
                        $('#result')
                            .html('An error occurred while processing your request')
                            .removeClass('spam not-spam')
                            .addClass('error')
                            .show();
                    }
                });
            });
        });
    </script>
</body>
</html>""")
        print(f"Created index.html template at: {index_html_path}")


if __name__ == "__main__":
    setup_project_structure()