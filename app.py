
        # DROPDOWNS FIXED
        # QUESTIONNAIRES APPEAR ON CORRECT TABS
        # LOGINS AND ACCOUNT CREATION DEBUGGED
        # PARAMETERS AND STATEMENTS TWEAKED
        # THEMES
        # ALLERGY QUESTION POP UP WORKS
        # LOGIN QUESTIONNAIRE POPS UP SAVING USER PREFERENCES FROM BEFORE

        # global dictionary to store existing usernames & passwords
        existing_users = {}
        # global dictionary to store user preferences
        user_preferences = {}

        # function to check if username is unique
        def is_unique(username):
            return username not in existing_users

        # function to create new account
        def create_account(username, password):
            if not username or not password:
                return "Username and password cannot be empty!", gr.Row.update(visible=False)  # hide questionnaire
            if username not in existing_users:
                existing_users[username] = password
                return "Account created successfully! You can now log in.", gr.Row.update(visible=True)  # show questionnaire
            else:
                return "Username is already taken. Please try a different one.", gr.Row.update(visible=False)  # keep questionnaire hidden

        # function to log in
        def login_user(username, password):
            if username in existing_users and existing_users[username] == password:
                return True, f"Welcome back, {username}!", gr.Row.update(visible=True)  # show questionnaire after login
            else:
                return False, "Invalid credentials. Please try again or create an account.", gr.Row.update(visible=False)

        def new_questions(q1_input, q2_input, q3_input, q4_input, q5_input, allergy_details=None):
            result = ""

            # Q1: Do you have any food allergies?
            if q1_input == 'yes':
                result += f"
You have reported the following allergies: {allergy_details}"
            else:
                result += '
No allergies reported.'

            # Q2: Cooking skill level (validated)
            if q2_input in ['1', '2', '3']:
                result += f"
Cooking skill level: {q2_input}"
            else:
                result += '
Invalid input for cooking skill level. Please enter 1, 2, or 3.'

            # Q3: How many recipes?
            if 1 <= q3_input <= 15:
                result += f"
Number of recipes: {q3_input}"
            else:
                result += '
Invalid input for number of recipes. Please enter a number between 1 and 15.'

            # Q4: How many servings?
            if 1 <= q4_input <= 50:
                result += f"
Number of servings: {q4_input}"
            else:
                result += '
Invalid input for servings. Please enter a number between 1 and 50.'

            # Q5: How much time for meal prep?
            if q5_input in range(0, 800, 5):
                result += f"
Meal prep time: {q5_input} minutes"
            else:
                result += '
Invalid input for time. Please enter a valid time in minutes.'

            return result

        def returning_questions(username, q2_input, q3_input, q4_input, q5_input):
            # ensure user preferences exist; otherwise, initialize them
            global user_preferences

            # preserve allergies
            allergies = user_preferences[username].get("allergies", "None")

            # start building result string
            result = f"Updating preferences for {username}:
"

            # Q2: Cooking skill level
            if q2_input in ['1', '2', '3']:
                result += f"Cooking skill level set to: {q2_input}
"
                user_preferences[username]['skill_level'] = q2_input
            else:
                result += "Invalid input for cooking skill level. Please enter 1, 2, or 3.
"

            # Q3: Number of recipes
            if 1 <= q3_input <= 15:
                result += f"Number of recipes set to: {q3_input}
"
                user_preferences[username]['recipes'] = q3_input
            else:
                result += "Invalid input for number of recipes. Please enter a number between 1 and 15.
"

            # Q4: Number of servings
            if 1 <= q4_input <= 50:
                result += f"Number of servings set to: {q4_input}
"
                user_preferences[username]['servings'] = q4_input
            else:
                result += "Invalid input for servings. Please enter a number between 1 and 50.
"

            # Q5: Meal prep time
            if q5_input in range(0, 800, 5):
                result += f"Meal prep time set to: {q5_input} minutes
"
                user_preferences[username]['prep_time'] = q5_input
            else:
                result += "Invalid input for prep time. Please enter a valid time in minutes (multiples of 5).
"

            # reapply allergies without changes
            user_preferences[username]['allergies'] = allergies
            result += f"Allergies retained: {allergies}"

            return result

        def create_app():
            html_content = """
              <style>
              .title-container {
                  display: flex;
                  align-items: center; /* Vertically align title and logo */
              }
              .logo {
                  margin-left: 10px;  /* Adjust spacing between title and logo */
              }
              .logo img {
                  border: none; /* Remove image border */
              }
              </style>
              <div class="title-container">
                  <h1>Welcome to MyRecipes!</h1>
                  <div class="logo">
                      <img src='/content/drive/MyDrive/CSC461/chefhat.png' width="50" height="50">
                  </div>
              </div>
              """  # HTML to remove image border

            with gr.Blocks(theme=gr.themes.Default(primary_hue="lime", secondary_hue="green", neutral_hue='cyan', spacing_size="sm", radius_size="none", text_size='lg')) as app:
                with gr.Row():
                    # site logo
                    gr.HTML(html_content)

                # tabs for login + account creation
                with gr.Tabs() as tabs:
                    with gr.Tab("Login"):
                        with gr.Row():
                            username_input = gr.Textbox(label="Username", placeholder="Enter your username")
                            password_input = gr.Textbox(label="Password", placeholder="Enter your password", type="password")
                            login_button = gr.Button("Login")
                            login_output = gr.Textbox(label="Login Status", interactive=False)

                    with gr.Tab("Create Account"):
                        with gr.Row():
                            new_username_input = gr.Textbox(label="New Username", placeholder="Enter a new username")
                            new_password_input = gr.Textbox(label="New Password", placeholder="Enter a new password", type="password")
                            create_account_button = gr.Button("Create Account")
                            create_account_output = gr.Textbox(label="Account Status", interactive=False)

                # after account creation, show User Questionnaire content
                user_questionnaire_row = gr.Row(visible=False)
                with user_questionnaire_row:
                    questionnaire_title = gr.Markdown("# New User Preferences")

                    # Q1: Do you have food allergies?
                    q1_input = gr.Radio(choices=["yes", "no"], label="Do you have any food allergies?")

                    # Q2: Cooking skill level
                    q2_input = gr.Dropdown(choices=["1", "2", "3"], label="What is your cooking skill level? (1=Beginner, 2=Intermediate, 3=Advanced)")

                    # Q3: How many recipes?
                    q3_input = gr.Number(label="How many recipes would you like to see?", value=1, interactive=True)

                    # Q4: How many servings?
                    q4_input = gr.Number(label="How many servings are desired?", value=1, interactive=True)

                    # Q5: How much time for meal prep?
                    q5_input = gr.Number(label="How much time (in minutes) do you want to spend on making the meal?", value=0, interactive=True)

                    # conditional question for allergies
                    allergy_details_input = gr.Textbox(label="Please list your food allergies:", visible=False)

                    submit_button = gr.Button("Submit")
                    output_text = gr.Textbox(label="Results", interactive=False)

                    # show allergy question only if user selects 'yes' for allergies
                    def show_allergy_question(q1_input):
                        if q1_input == 'yes':
                            return gr.update(visible=True)
                        else:
                            return gr.update(visible=False)

                    q1_input.change(show_allergy_question, inputs=[q1_input], outputs=[allergy_details_input])

                    submit_button.click(
                        new_questions,
                        inputs=[q1_input, q2_input, q3_input, q4_input, q5_input, allergy_details_input],
                        outputs=output_text,
                    )

                # login questionnaire (visible only after login)
                login_questionnaire_row = gr.Row(visible=False)
                with login_questionnaire_row:
                    questionnaire_title = gr.Markdown("# Recipe Suggestion Preferences")
                    q2_input_login = gr.Dropdown(choices=["1", "2", "3"], label="What is your cooking skill level? (1=Beginner, 2=Intermediate, 3=Advanced)")
                    q3_input_login = gr.Number(label="How many recipes would you like to see (up to 15)?", value=1)
                    q4_input_login = gr.Number(label="How many servings are desired?", value=1)
                    q5_input_login = gr.Number(label="How much time (in minutes) do you want to spend on making the meal?", value=0)

                    submit_login_button = gr.Button("Submit")
                    login_output_text = gr.Textbox(label="Results", interactive=False)

                    submit_login_button.click(
                        returning_questions,
                        inputs=[username_input, q2_input_login, q3_input_login, q4_input_login, q5_input_login],
                        outputs=login_output_text,
                    )

                # handlers to reset visibility
                def reset_questionnaire_visibility():
                    return gr.Row.update(visible=False), gr.Row.update(visible=False)

                tabs.change(
                    reset_questionnaire_visibility,
                    inputs=[],
                    outputs=[user_questionnaire_row, login_questionnaire_row],
                )

                # account creation handler
                def create_account_handler(username, password):
                    message, visibility_update = create_account(username, password)
                    # show questionnaire only if account creation successful
                    return message, visibility_update

                create_account_button.click(
                    create_account_handler,
                    inputs=[new_username_input, new_password_input],
                    outputs=[create_account_output, user_questionnaire_row],
                )

                # login handler
                def login_handler(username, password):
                    success, message, visibility_update = login_user(username, password)
                    if success:
                        # only show preferences update section when login is successful
                        return message, gr.Row.update(visible=True)  # show questionnaire
                    else:
                        return message, gr.Row.update(visible=False)  # hide questionnaire if login fails

                # correct button for login
                login_button.click(
                    login_handler,
                    inputs=[username_input, password_input],
                    outputs=[login_output, user_questionnaire_row],
                )

                # fix submit button in the login phase to update preferences
                submit_login_button.click(
                    returning_questions,
                    inputs=[username_input, q2_input_login, q3_input_login, q4_input_login, q5_input_login],
                    outputs=login_output_text,  # Show results
                )

            return app

        # launch interface
        interface = create_app()
        interface.launch(share=False)
    