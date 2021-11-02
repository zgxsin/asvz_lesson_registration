# ASVZ Lesson Registration
This script registers for the ASVZ lesson automatically.

## Get Started
Update line 32 and line 36 with your ASVZ membership username and password respectively:
```
   login_user_name.send_keys("your_username")
   login_password.send_keys("your_password")
```
Go to the ASVZ website and find the lesson ID. For example, the lesson ID is 241073 for this lesson: https://schalter.asvz.ch/tn/lessons/241073.
Afterwards, run the following command
`python3 register_for_asvz_lesson.py -i 241073` to register for this lesson.