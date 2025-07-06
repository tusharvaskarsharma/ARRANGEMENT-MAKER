# 🗓️ School Timetable Arrangement System

A Python program for automatically generating substitute timetables when teachers are absent. It helps schools maintain smooth operations by reassigning periods from absent teachers to available staff in a fair and efficient manner.

---

## 🚀 Features

- Detects the current day and loads the relevant timetable automatically
- Interactive CLI menu for marking teachers as absent
- Identifies which periods require substitute teachers
- Distributes substitute duties fairly among present teachers
- Saves the new arrangement to a CSV file
- Displays the final arrangement in a neat table format

> **Note:** This version does **not** store data in any SQL database.

---
<hr>
## 📂 Project Structure

project <br>
│ <br>
├── Monday.csv <br>
├── Tuesday.csv<br>
├── Wednesday.csv<br>
├── Thursday.csv<br>
├── Friday.csv<br>
├── Saturday.csv<br>
│<br>
├── ARRANGEMENT.CSV<br>
│<br>
└── timetable_arrangement.py<br>

<br>

---

## 📑 Timetable CSV Format

Each weekday has a CSV file named like `Monday.csv`.

- The first row is a header and is ignored by the program.
- Each subsequent row represents one teacher’s schedule for that day.

Example (`Monday.csv`):

| TEACHER   | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|-----------|---|---|---|---|---|---|---|---|
| Mrs. Roy  | 8A | 7B |   |   | 9C |   |   |   |
| Mr. Singh |   | 9A | 6C |   |   | 7A |   |   |

- Empty cells indicate free periods.

---

## 💻 How It Works

1. **Identifies the Current Day**

   - Uses Python’s `datetime` module to determine today’s day name.
   - Loads the matching CSV file for that day.

2. **Loads Timetable Data**

   - Reads the timetable into a list of lists.

3. **Marks Absent Teachers**

   - Presents a numbered list of teachers.
   - User selects absent teachers by entering their serial numbers.

4. **Identifies Substitute Requirements**

   - Determines which periods the absent teachers were scheduled to teach.

5. **Finds Available Substitutes**

   - Looks for present teachers free during those periods.
   - Prefers teachers with fewer total classes for fair distribution.
   - Randomly chooses among eligible teachers.

6. **Generates Final Arrangement**

   - Builds a new arrangement showing substitute allocations.
   - Saves the arrangement to `ARRANGEMENT.CSV`.
   - Displays the arrangement as a formatted table in the terminal.

---

TEACHERS,1              ,2            ,3,4,            5,6,7,8 <br>
Mrs. Roy,Mr. Singh in 8A,Mr. Das in 7B,, ,Mr. Paul in 9C,,,<br>
...

## 💾 Output

### `ARRANGEMENT.CSV`

Stores the updated timetable for absent teachers:


Also prints a neat table, e.g.:

+-------------+-------------------+-------------------+-----+-----+-------------------+-----+-----+-----+<br>
| TEACHER     | 1ST               | 2ND               | 3RD | 4TH | 5TH               | 6TH | 7TH | 8TH |<br>
+-------------+-------------------+-------------------+-----+-----+-------------------+-----+-----+-----+<br>
| Mrs. Roy    | Mr. Singh in 8A   | Mr. Das in 7B     |     |     | Mr. Paul in 9C    |     |     |     |<br>
+-------------+-------------------+-------------------+-----+-----+-------------------+-----+-----+-----+<br>


---

## 🛠 Requirements

- Python 3.x
- [tabulate](https://pypi.org/project/tabulate/)

Install dependencies:

```bash
pip install tabulate
```

⚙️ How to Run
Prepare your CSV timetable files (e.g. Monday.csv, Tuesday.csv) in the same directory.

Run the program:
```bash
python timetable_arrangement.py
```
<br>
Follow the on-screen prompts to:

Select absent teachers
<br>
Review the generated arrangement
<br><br><br>
✏️ Customization<br><br>
Edit the CSV files to reflect your school’s actual timetable.

Adjust the number of periods (currently 8) if your school has more or fewer classes.
<br><br>
<br>
Happy Scheduling! 🎒
<br><br>

-TUSHAR

