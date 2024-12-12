
# HUMANS - Human Resource Utilization and Management Automated Network

The "Human Resource Utilization and Management Automated Network" refers to a digital system designed to streamline and automate various aspects of human resource (HR) management within an organization. This network integrates HR processes such as recruitment, employee onboarding, performance management, payroll, benefits administration, and workforce planning. By automating these tasks, the system enhances efficiency, reduces manual errors, and provides real-time data for better decision-making. It also helps in optimizing the utilization of human resources by ensuring that employees are effectively allocated, their skills are matched to appropriate tasks, and their performance is monitored and improved through data-driven insights.


## Documentation

An explanation of the phrase "Human Resource Utilization and Management Automated Network" broken down by each key term:

1. Human Resource: Refers to the employees or workforce of an organization, encompassing all personnel who contribute to the company's operations, including their skills, abilities, and experience.

2. Utilization: The effective and efficient use of resources—in this context, the workforce. It involves optimizing how employees' time, skills, and abilities are employed to meet organizational goals.

3. Management: The process of overseeing and coordinating the activities of the workforce, including hiring, training, evaluating performance, and ensuring that employees are aligned with the organization’s objectives.

4. Automated: The use of technology to perform tasks with minimal human intervention. In HR, this could mean automating processes like payroll, attendance tracking, or performance reviews, increasing efficiency and accuracy.

5. Network: A system or framework that connects various elements or components. In this context, it refers to a digital platform or system that links different HR functions, allowing for integrated management and data sharing across the organization.

6. System: A structured set of processes and tools designed to perform specific functions. Here, it refers to the overall technological framework that supports the automation, management, and networking of HR activities, ensuring they operate in a coordinated and efficient manner.
## Tech Stack

**Client:** Django (Python 3.8, 3.9, 3.10) and Bootstrap 5

**Web Template:** Metronic 8

**Server:** MySql


## Installation
Requirements

Build assets

```bash
  cd /humans/_keenthemes/tools directory
  npm install
  gulp
```

Django development

```bash
  cd /humans/ directory
  python -m venv env // only create this environment if you dont have
    
  .\env\Scripts\activate //cmd
  or
  source env/Scripts/activate //bash

  python -m pip install django
  pip install -r requirements.txt
  python manage.py migrate
  python manage.py runserver
```


## Installation

```bash
  python -m venv .venv
```
```bash
pip install -r requirements.txt
```

```bash
npm install
```

```bash
npm run dev
```

```bash
python manage.py migrate
```

```bash
python manage.py runserver
```
## Production

```bash
npm run build
```

```bash
python manage.py collectstatic
```

```bash
python manage.py runserver
```

## Custom Commands

#### Get Newly Hired From IRIS
- can be used for crons or sync button

<<<<<<< HEAD
```bash
python manage.py fetch_hired_applicants
```

=======
```http
 python manage.py fetch_hired_applicants
```


>>>>>>> a9f93740febb7003aba72238e1131145fce5d783
