# ASVZ Lesson Registration
This script registers for the ASVZ lesson automatically.

## Get Started
### Use the ASVZ membership Account
Update line 36 and line 40 with the ASVZ membership username and password respectively:
```
   login_user_name.send_keys("your_username")
   login_password.send_keys("your_password")
```
### Use the University Account
Update the university in line 52. Currently, only `ETH Zurich` is supported. Please open an issue if you need support for other universities.
```bash
 aai_portal = driver.find_element(By.XPATH, "//div[@title='Universities: ETH Zurich']")
```
Also update line 60 and line 62 with the University account username and password respectively.

Go to the ASVZ website and find the lesson ID. For example, the lesson ID is 241073 for this lesson: https://schalter.asvz.ch/tn/lessons/241073.
Afterwards, run the following command
`python3 register_for_asvz_lesson.py -i 241073` to register for this lesson.