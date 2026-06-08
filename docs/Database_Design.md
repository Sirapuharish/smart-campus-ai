# Database Design

## Student

- student_id
- name
- email
- password
- class
- section

---

## Teacher

- teacher_id
- name
- email
- password
- subject

---

## Principal

- principal_id
- name
- email
- password

---

## Material

- material_id
- title
- uploaded_by
- file_path
- upload_date

---

## Quiz

- quiz_id
- title
- created_by
- subject

---

## Question

- question_id
- quiz_id
- question_text
- option_a
- option_b
- option_c
- option_d
- correct_answer

---

## Result

- result_id
- student_id
- quiz_id
- score
- submission_date