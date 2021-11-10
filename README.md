# ASVZ Lesson Registration
This script registers for the ASVZ lesson automatically.

## Get Started
### Use the ASVZ membership Account
Update the line below with the ASVZ membership account username and password:
```bash
    asvz_account_login(driver, "your_username", "your_password")
```
### Use the University Account
Currently, only `ETH Zurich` is supported. Please open an issue if you need support for other universities.
Update the line below with the University account username and password.
```bash
  asvz_eth_portal_login(driver, "your_username", "your_password")
```

Go to the ASVZ website and find the lesson ID. For example, the lesson ID is 241073 for this lesson: https://schalter.asvz.ch/tn/lessons/241073.
Afterwards, run the following command
`python3 register_for_asvz_lesson.py -i 241073` to register for this lesson.